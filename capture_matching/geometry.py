"""Local geometry for capture matching.

Positions stay in WGS84. Costs are computed in a local east-north frame,
which is the equirectangular approximation of geodesic distance and is
accurate to well under a meter at the ranges used here (tens of meters).
"""

from __future__ import annotations

import math

import numpy as np

EARTH_RADIUS_M = 6_371_000.0
METERS_PER_DEGREE = 2.0 * math.pi * EARTH_RADIUS_M / 360.0


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in meters."""
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = (
        math.sin(d_phi / 2.0) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2.0) ** 2
    )
    return 2.0 * EARTH_RADIUS_M * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))


def offset_latlon(
    lat: float, lon: float, east_m: float, north_m: float
) -> tuple[float, float]:
    """Move a WGS84 point by an east/north offset in meters."""
    lat2 = lat + north_m / METERS_PER_DEGREE
    cos_lat = max(0.01, math.cos(math.radians(lat)))
    lon2 = lon + east_m / (METERS_PER_DEGREE * cos_lat)
    return lat2, lon2


def to_local_xy(
    lat: float, lon: float, origin_lat: float, origin_lon: float
) -> tuple[float, float]:
    """Project one point to meters east and north of an origin."""
    north = (lat - origin_lat) * METERS_PER_DEGREE
    cos_lat = max(0.01, math.cos(math.radians(origin_lat)))
    east = (lon - origin_lon) * METERS_PER_DEGREE * cos_lat
    return east, north


def project_captures(
    lats: np.ndarray,
    lons: np.ndarray,
    origin_lat: float,
    origin_lon: float,
) -> np.ndarray:
    """Project arrays of lat/lon to an (n, 2) east-north array."""
    north = (lats - origin_lat) * METERS_PER_DEGREE
    cos_lat = max(0.01, math.cos(math.radians(origin_lat)))
    east = (lons - origin_lon) * METERS_PER_DEGREE * cos_lat
    return np.column_stack((east, north))


def knn_distances(xy: np.ndarray, index: int, k: int = 3) -> np.ndarray:
    """Sorted distances from one point to its k nearest session neighbors.

    The multiset of neighbor distances is translation-invariant, so two
    visits to the same tree share it even when the whole session is shifted.
    """
    if len(xy) <= 1:
        return np.zeros(0, dtype=float)
    delta = xy - xy[index]
    dist = np.linalg.norm(delta, axis=1)
    others = np.sort(dist[np.arange(len(xy)) != index])
    return others[:k]


def signature_delta(left: np.ndarray, right: np.ndarray) -> float:
    """Mean absolute difference of the shortest shared neighbor distances."""
    if len(left) == 0 or len(right) == 0:
        return 0.0
    n = min(len(left), len(right))
    return float(np.mean(np.abs(left[:n] - right[:n])))


def _unique_inlier_stats(
    xy_a: np.ndarray, xy_b_aligned: np.ndarray, thresh_m: float
) -> tuple[int, float]:
    """Count a 1-1 pairing inside ``thresh_m`` and sum its squared residuals.

    A regular planting can admit two shifts with the same inlier count
    (the true offset, and one tree-spacing off). The smaller residual sum
    is the shift that actually lands on the trees.
    """
    if len(xy_a) == 0 or len(xy_b_aligned) == 0:
        return 0, 0.0
    dist = np.linalg.norm(xy_a[:, None, :] - xy_b_aligned[None, :, :], axis=2)
    pairs = np.argwhere(dist <= thresh_m)
    if len(pairs) == 0:
        return 0, 0.0
    order = np.argsort(dist[pairs[:, 0], pairs[:, 1]])
    used_a: set[int] = set()
    used_b: set[int] = set()
    count = 0
    sse = 0.0
    for idx in order:
        i = int(pairs[idx, 0])
        j = int(pairs[idx, 1])
        if i in used_a or j in used_b:
            continue
        used_a.add(i)
        used_b.add(j)
        count += 1
        sse += float(dist[i, j]) ** 2
    return count, sse


def estimate_translation(
    xy_a: np.ndarray,
    xy_b: np.ndarray,
    max_shift_m: float = 40.0,
    inlier_m: float = 8.0,
) -> np.ndarray:
    """Estimate the east/north bias of session B relative to session A.

    A single tracking session shares one GPS offset. Subtracting that bias
    from B is a translation (not a rotation): ``xy_b - bias ≈ xy_a``.

    Hypotheses are the session centroid and every point pair whose raw
    separation is inside ``max_shift_m``. The hypothesis with the most
    unique inliers wins, then a few mean-shift updates tighten it.
    """
    if len(xy_a) == 0 or len(xy_b) == 0:
        return np.zeros(2, dtype=float)

    centroid = xy_b.mean(axis=0) - xy_a.mean(axis=0)
    hypotheses: list[np.ndarray] = []
    if float(np.linalg.norm(centroid)) <= max_shift_m:
        hypotheses.append(centroid)
    for i in range(len(xy_a)):
        delta = xy_b - xy_a[i]
        norms = np.linalg.norm(delta, axis=1)
        for j in np.flatnonzero(norms <= max_shift_m):
            hypotheses.append(delta[int(j)])
    if not hypotheses:
        return np.zeros(2, dtype=float)

    best_bias = np.asarray(hypotheses[0], dtype=float)
    best_count = -1
    best_sse = float("inf")
    for bias in hypotheses:
        count, sse = _unique_inlier_stats(xy_a, xy_b - np.asarray(bias), inlier_m)
        if count > best_count or (count == best_count and sse < best_sse):
            best_count = count
            best_sse = sse
            best_bias = np.asarray(bias, dtype=float)

    bias = best_bias.copy()
    for _ in range(4):
        aligned = xy_b - bias
        dist = np.linalg.norm(xy_a[:, None, :] - aligned[None, :, :], axis=2)
        pairs = np.argwhere(dist <= inlier_m)
        if len(pairs) == 0:
            break
        order = np.argsort(dist[pairs[:, 0], pairs[:, 1]])
        used_a: set[int] = set()
        used_b: set[int] = set()
        residuals: list[np.ndarray] = []
        for idx in order:
            i = int(pairs[idx, 0])
            j = int(pairs[idx, 1])
            if i in used_a or j in used_b:
                continue
            used_a.add(i)
            used_b.add(j)
            residuals.append(xy_b[j] - xy_a[i])
        if not residuals:
            break
        bias = np.mean(residuals, axis=0)
    if float(np.linalg.norm(bias)) > max_shift_m:
        return np.zeros(2, dtype=float)
    return bias
