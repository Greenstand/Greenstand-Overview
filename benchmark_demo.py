"""Synthetic benchmark for the capture pre-matcher.

Builds a 20-tree zig-zag, shifts the second visit, adds GPS noise, and
prints precision and recall of the recovered pairs.

Run from the repository root::

    python benchmark_demo.py
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import numpy as np

from capture_matching.geometry import offset_latlon
from capture_matching.matcher import MatchEngine

ORIGIN_LAT = 8.48
ORIGIN_LON = -13.27


def _capture(tree_id: str, east_m: float, north_m: float, when: datetime) -> dict:
    lat, lon = offset_latlon(ORIGIN_LAT, ORIGIN_LON, east_m, north_m)
    return {
        "id": tree_id,
        "lat": lat,
        "lon": lon,
        "timestamp": when,
        "planter_id": "bench",
        "attributes": {},
    }


def build_sessions(
    n_trees: int = 20,
    spacing_m: float = 12.0,
    zig_zag_m: float = 8.0,
    translation_east_m: float = 11.0,
    translation_north_m: float = -6.0,
    noise_sigma_m: float = 1.5,
    seed: int = 42,
) -> tuple[list[dict], list[dict], set[tuple[str, str]]]:
    """Return session A, drifted session B, and the true id pairs."""
    rng = np.random.default_rng(seed)
    start = datetime(2023, 6, 13, 9, 0, tzinfo=timezone.utc)
    session_a: list[dict] = []
    session_b: list[dict] = []
    truth: set[tuple[str, str]] = set()
    for index in range(n_trees):
        tree_id = f"t{index:02d}"
        east = index * spacing_m
        north = zig_zag_m if index % 2 else 0.0
        when_a = start + timedelta(seconds=40 * index)
        when_b = start + timedelta(days=28, seconds=40 * index)
        session_a.append(_capture(tree_id, east, north, when_a))
        noise = rng.normal(0.0, noise_sigma_m, size=2)
        session_b.append(
            _capture(
                tree_id,
                east + translation_east_m + float(noise[0]),
                north + translation_north_m + float(noise[1]),
                when_b,
            )
        )
        truth.add((tree_id, tree_id))
    return session_a, session_b, truth


def score(matches: list[tuple[str, str]], truth: set[tuple[str, str]]) -> tuple[float, float]:
    """Precision and recall against the planted pairs."""
    predicted = set(matches)
    if not predicted:
        precision = 0.0
    else:
        precision = len(predicted & truth) / len(predicted)
    recall = 0.0 if not truth else len(predicted & truth) / len(truth)
    return precision, recall


def main() -> None:
    session_a, session_b, truth = build_sessions()
    result = MatchEngine().match(session_a, session_b)
    predicted = [(str(item.id_a), str(item.id_b)) for item in result.matches]
    precision, recall = score(predicted, truth)
    print(f"trees={len(session_a)}")
    print(
        "estimated_translation_m="
        f"{result.translation_east_m:.2f},{result.translation_north_m:.2f}"
    )
    print(f"matches={len(result.matches)}")
    print(f"precision={precision:.3f}")
    print(f"recall={recall:.3f}")


if __name__ == "__main__":
    main()
