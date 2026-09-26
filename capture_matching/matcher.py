"""Cross-session capture pre-matching.

Two visits to the same planting share a walking constellation. Cheap GPS
adds a session-wide translation of a few meters to about 15 m, which is
larger than the gap between neighboring trees. This module estimates that
one shift, then assigns captures 1-to-1.

The pairwise cost, in meters, is

    C_ij = w_d * d_ij + w_s * s_ij + w_h * h_ij + w_t * t_ij

where ``d_ij`` is the haversine residual after the shift is removed,
``s_ij`` is the absolute difference of normalized walking order,
``h_ij`` is the heading disagreement of the step into each capture,
and ``t_ij`` is the difference of k-nearest-neighbor distance signatures.
Pairs farther than the search radius are not eligible. The Hungarian
algorithm may also leave a capture unmatched when every candidate is worse
than the rejection cost.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Sequence

import numpy as np
from scipy.optimize import linear_sum_assignment

from capture_matching.geometry import (
    estimate_translation,
    haversine_m,
    knn_distances,
    offset_latlon,
    project_captures,
    signature_delta,
)

PROHIBITIVE_COST = 1.0e6


@dataclass
class Capture:
    """One geotagged tree capture."""

    id: str | int
    lat: float
    lon: float
    timestamp: datetime
    planter_id: str | None = None
    attributes: dict[str, Any] = field(default_factory=dict)


@dataclass
class Match:
    """One accepted link between a capture in A and a capture in B."""

    id_a: str | int
    id_b: str | int
    confidence: float
    distance_m: float
    cost: float


@dataclass
class MatchResult:
    """Assignment of session B onto session A."""

    matches: list[Match]
    unmatched_a: list[str | int]
    unmatched_b: list[str | int]
    translation_east_m: float
    translation_north_m: float


def _parse_time(value: datetime | str | None, fallback_index: int) -> datetime:
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value
    if isinstance(value, str) and value:
        text = value.replace("Z", "+00:00")
        parsed = datetime.fromisoformat(text)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed
    return datetime(1970, 1, 1, tzinfo=timezone.utc).replace(second=min(fallback_index, 59))


def as_capture(raw: Capture | Mapping[str, Any], fallback_index: int = 0) -> Capture:
    """Accept a :class:`Capture` or a dict with the documented keys."""
    if isinstance(raw, Capture):
        return raw
    attributes = raw.get("attributes") or {}
    planter = raw.get("planter_id")
    return Capture(
        id=raw["id"],
        lat=float(raw["lat"]),
        lon=float(raw["lon"]),
        timestamp=_parse_time(raw.get("timestamp"), fallback_index),
        planter_id=None if planter is None else str(planter),
        attributes=dict(attributes),
    )


def _step_heading(xy: np.ndarray, index: int) -> np.ndarray | None:
    if index == 0:
        return None
    step = xy[index] - xy[index - 1]
    length = float(np.linalg.norm(step))
    if length < 0.5:
        return None
    return step / length


def _heading_penalty(heading_a: np.ndarray | None, heading_b: np.ndarray | None) -> float:
    """0 when the incoming steps agree, 1 when they point opposite ways."""
    if heading_a is None or heading_b is None:
        return 0.0
    dot = float(np.clip(np.dot(heading_a, heading_b), -1.0, 1.0))
    return (1.0 - dot) / 2.0


def _boxes_overlap(
    session_a: Sequence[Capture],
    session_b: Sequence[Capture],
    margin_m: float,
) -> bool:
    a_lat = [c.lat for c in session_a]
    a_lon = [c.lon for c in session_a]
    b_lat = [c.lat for c in session_b]
    b_lon = [c.lon for c in session_b]
    mid_lat = (min(a_lat) + max(a_lat) + min(b_lat) + max(b_lat)) / 4.0
    d_lat = margin_m / 111_320.0
    cos_lat = max(0.2, math.cos(math.radians(mid_lat)))
    d_lon = margin_m / (111_320.0 * cos_lat)
    if max(a_lat) + d_lat < min(b_lat) - d_lat or max(b_lat) + d_lat < min(a_lat) - d_lat:
        return False
    if max(a_lon) + d_lon < min(b_lon) - d_lon or max(b_lon) + d_lon < min(a_lon) - d_lon:
        return False
    return True


class MatchEngine:
    """Link captures from two tracking sessions.

    Parameters
    ----------
    max_search_radius_m:
        Residual geodesic distance above which a pair is not a candidate.
    max_shift_m:
        Largest session-wide GPS bias the alignment is allowed to remove.
    min_confidence:
        Assignments below this score are returned as unmatched.
    weights:
        ``(distance, sequence, heading, topology)``. Sequence and heading
        are on ``[0, 1]`` and are scaled into meters by their weights.
    """

    def __init__(
        self,
        max_search_radius_m: float = 25.0,
        max_shift_m: float = 40.0,
        min_confidence: float = 0.35,
        weights: tuple[float, float, float, float] = (1.0, 4.0, 3.0, 0.75),
        species_penalty_m: float = 20.0,
    ) -> None:
        self.max_search_radius_m = max_search_radius_m
        self.max_shift_m = max_shift_m
        self.min_confidence = min_confidence
        self.w_distance, self.w_sequence, self.w_heading, self.w_topology = weights
        self.species_penalty_m = species_penalty_m
        self._tau = max_search_radius_m * 0.45

    def match(
        self,
        session_a: Sequence[Capture | Mapping[str, Any]],
        session_b: Sequence[Capture | Mapping[str, Any]],
    ) -> MatchResult:
        """Return the 1-to-1 pre-matches of ``session_b`` onto ``session_a``."""
        captures_a = self._prepare(session_a)
        captures_b = self._prepare(session_b)
        empty = MatchResult([], [c.id for c in captures_a], [c.id for c in captures_b], 0.0, 0.0)
        if not captures_a or not captures_b:
            return empty
        margin = self.max_shift_m + self.max_search_radius_m
        if not _boxes_overlap(captures_a, captures_b, margin):
            return empty

        origin_lat = float(np.mean([c.lat for c in captures_a]))
        origin_lon = float(np.mean([c.lon for c in captures_a]))
        xy_a = project_captures(
            np.array([c.lat for c in captures_a]),
            np.array([c.lon for c in captures_a]),
            origin_lat,
            origin_lon,
        )
        xy_b = project_captures(
            np.array([c.lat for c in captures_b]),
            np.array([c.lon for c in captures_b]),
            origin_lat,
            origin_lon,
        )
        bias = estimate_translation(xy_a, xy_b, self.max_shift_m, inlier_m=8.0)
        cost, residual = self._cost_matrix(captures_a, captures_b, xy_a, xy_b, bias)
        pairs = self._assign(cost)
        matches: list[Match] = []
        matched_a: set[int] = set()
        matched_b: set[int] = set()
        for i, j in pairs:
            pair_cost = float(cost[i, j])
            confidence = self._confidence(pair_cost)
            if confidence < self.min_confidence or residual[i, j] > self.max_search_radius_m:
                continue
            matches.append(
                Match(
                    id_a=captures_a[i].id,
                    id_b=captures_b[j].id,
                    confidence=confidence,
                    distance_m=float(residual[i, j]),
                    cost=pair_cost,
                )
            )
            matched_a.add(i)
            matched_b.add(j)
        matches.sort(key=lambda item: (-item.confidence, str(item.id_a)))
        return MatchResult(
            matches=matches,
            unmatched_a=[c.id for i, c in enumerate(captures_a) if i not in matched_a],
            unmatched_b=[c.id for j, c in enumerate(captures_b) if j not in matched_b],
            translation_east_m=float(bias[0]),
            translation_north_m=float(bias[1]),
        )

    def _prepare(self, session: Sequence[Capture | Mapping[str, Any]]) -> list[Capture]:
        captures = [as_capture(raw, index) for index, raw in enumerate(session)]
        captures.sort(key=lambda c: (c.timestamp, str(c.id)))
        return captures

    def _confidence(self, cost: float) -> float:
        """Map a meter-valued cost onto ``(0, 1]``. A zero residual scores 1."""
        if cost >= PROHIBITIVE_COST / 10.0:
            return 0.0
        return float(math.exp(-cost / self._tau))

    def _reject_cost(self) -> float:
        """Cost whose confidence equals ``min_confidence``."""
        floor = min(max(self.min_confidence, 1.0e-6), 1.0 - 1.0e-6)
        return -self._tau * math.log(floor)

    def _cost_matrix(
        self,
        captures_a: Sequence[Capture],
        captures_b: Sequence[Capture],
        xy_a: np.ndarray,
        xy_b: np.ndarray,
        bias: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray]:
        n = len(captures_a)
        m = len(captures_b)
        cost = np.full((n, m), PROHIBITIVE_COST, dtype=float)
        residual = np.full((n, m), PROHIBITIVE_COST, dtype=float)
        sig_a = [knn_distances(xy_a, i) for i in range(n)]
        sig_b = [knn_distances(xy_b, j) for j in range(m)]
        head_a = [_step_heading(xy_a, i) for i in range(n)]
        head_b = [_step_heading(xy_b, j) for j in range(m)]
        denom_a = max(n - 1, 1)
        denom_b = max(m - 1, 1)
        east = -float(bias[0])
        north = -float(bias[1])
        for i, cap_a in enumerate(captures_a):
            for j, cap_b in enumerate(captures_b):
                lat_b, lon_b = offset_latlon(cap_b.lat, cap_b.lon, east, north)
                dist = haversine_m(cap_a.lat, cap_a.lon, lat_b, lon_b)
                residual[i, j] = dist
                if dist > self.max_search_radius_m:
                    continue
                sequence = abs(i / denom_a - j / denom_b)
                heading = _heading_penalty(head_a[i], head_b[j])
                topo = signature_delta(sig_a[i], sig_b[j])
                species = self._species_penalty(cap_a, cap_b)
                cost[i, j] = (
                    self.w_distance * dist
                    + self.w_sequence * sequence
                    + self.w_heading * heading
                    + self.w_topology * topo
                    + species
                )
        return cost, residual

    def _species_penalty(self, cap_a: Capture, cap_b: Capture) -> float:
        species_a = cap_a.attributes.get("species")
        species_b = cap_b.attributes.get("species")
        if species_a and species_b and species_a != species_b:
            return self.species_penalty_m
        return 0.0

    def _assign(self, cost: np.ndarray) -> list[tuple[int, int]]:
        """Hungarian assignment that may leave either side unmatched.

        Each row gets a private dummy column priced at the rejection cost.
        A real pair is chosen only when it is cheaper than staying unmatched.
        """
        n, m = cost.shape
        if n == 0 or m == 0:
            return []
        reject = self._reject_cost()
        padded = np.full((n, m + n), reject, dtype=float)
        padded[:, :m] = cost
        row_ind, col_ind = linear_sum_assignment(padded)
        chosen: list[tuple[int, int]] = []
        for i, j in zip(row_ind, col_ind):
            if int(j) < m:
                chosen.append((int(i), int(j)))
        return chosen
