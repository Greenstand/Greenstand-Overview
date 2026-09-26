"""Unit tests for cross-session capture pre-matching."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import numpy as np
import pytest

from benchmark_demo import build_sessions, score
from capture_matching.geometry import haversine_m, offset_latlon
from capture_matching.matcher import MatchEngine

ORIGIN = (8.48, -13.27)
START = datetime(2023, 6, 13, 10, 0, tzinfo=timezone.utc)


def _point(tree_id: str, east: float, north: float, minute: int, **extra: object) -> dict:
    lat, lon = offset_latlon(ORIGIN[0], ORIGIN[1], east, north)
    payload = {
        "id": tree_id,
        "lat": lat,
        "lon": lon,
        "timestamp": START + timedelta(minutes=minute),
        "planter_id": "grower-1",
        "attributes": {},
    }
    payload.update(extra)
    return payload


def _pair_ids(result) -> set[tuple[object, object]]:
    return {(item.id_a, item.id_b) for item in result.matches}


def test_haversine_one_degree_of_latitude() -> None:
    expected = 2.0 * np.pi * 6_371_000.0 / 360.0
    assert haversine_m(0.0, 0.0, 1.0, 0.0) == pytest.approx(expected, rel=1e-6)


def test_identical_coordinates_match_one_to_one() -> None:
    shared = [(0.0, 0.0), (16.0, 1.0), (32.0, -1.0), (48.0, 2.0)]
    session_a = [_point(f"a{i}", e, n, i) for i, (e, n) in enumerate(shared)]
    session_b = [_point(f"b{i}", e, n, i + 10) for i, (e, n) in enumerate(shared)]
    # Deliver B in reverse so the engine has to sort by time itself.
    result = MatchEngine().match(session_a, list(reversed(session_b)))
    assert _pair_ids(result) == {(f"a{i}", f"b{i}") for i in range(4)}
    assert result.unmatched_a == []
    assert result.unmatched_b == []
    assert all(item.confidence > 0.9 for item in result.matches)
    assert all(item.distance_m < 0.5 for item in result.matches)


def test_systematic_northeast_offset_is_removed() -> None:
    layout = [(0.0, 0.0), (14.0, 6.0), (28.0, 0.5), (42.0, 7.0), (56.0, 1.0)]
    session_a = [_point(f"a{i}", e, n, i) for i, (e, n) in enumerate(layout)]
    session_b = [
        _point(f"b{i}", e + 10.0, n + 10.0, i) for i, (e, n) in enumerate(layout)
    ]
    result = MatchEngine().match(session_a, session_b)
    assert _pair_ids(result) == {(f"a{i}", f"b{i}") for i in range(5)}
    assert result.translation_east_m == pytest.approx(10.0, abs=1.5)
    assert result.translation_north_m == pytest.approx(10.0, abs=1.5)
    assert max(item.distance_m for item in result.matches) < 1.5


def test_jitter_under_three_meters_keeps_true_pairs() -> None:
    rng = np.random.default_rng(7)
    n_trees = 8
    session_a = []
    session_b = []
    for i in range(n_trees):
        east = i * 15.0
        north = 4.0 if i % 2 else 0.0
        session_a.append(_point(f"a{i}", east, north, i))
        noise = rng.uniform(-1.8, 1.8, size=2)
        session_b.append(_point(f"b{i}", east + float(noise[0]), north + float(noise[1]), i))
    result = MatchEngine().match(session_a, session_b)
    assert _pair_ids(result) == {(f"a{i}", f"b{i}") for i in range(n_trees)}
    assert min(item.confidence for item in result.matches) > 0.55


def test_missing_trees_and_outlier_stay_unmatched() -> None:
    layout = [(0.0, 0.0), (18.0, 2.0), (36.0, 0.0), (54.0, 3.0), (72.0, 0.5), (90.0, 2.5)]
    session_a = [_point(f"a{i}", e, n, i) for i, (e, n) in enumerate(layout)]
    # B revisits the middle four, and one capture is a bad fix far away.
    kept = [1, 2, 3, 4]
    session_b = [_point(f"b{i}", layout[i][0] + 4.0, layout[i][1] - 3.0, i) for i in kept]
    session_b.append(_point("outlier", 400.0, 400.0, 20))
    result = MatchEngine().match(session_a, session_b)
    assert _pair_ids(result) == {(f"a{i}", f"b{i}") for i in kept}
    assert set(result.unmatched_a) == {"a0", "a5"}
    assert result.unmatched_b == ["outlier"]


def test_empty_and_distant_sessions_match_nothing() -> None:
    engine = MatchEngine()
    one = [_point("a", 0.0, 0.0, 0)]
    assert engine.match([], []).matches == []
    assert engine.match(one, []).unmatched_a == ["a"]
    assert engine.match([], one).unmatched_b == ["a"]
    far = [_point("far", 5_000.0, 0.0, 0)]
    result = engine.match(one, far)
    assert result.matches == []
    assert result.unmatched_a == ["a"]
    assert result.unmatched_b == ["far"]


def test_species_breaks_a_tie_against_a_closer_wrong_label() -> None:
    session_a = [_point("teak", 0.0, 0.0, 0, attributes={"species": "teak"})]
    session_b = [
        _point("right", 8.0, 0.0, 0, attributes={"species": "teak"}),
        _point("near", 2.0, 0.0, 1, attributes={"species": "neem"}),
    ]
    result = MatchEngine().match(session_a, session_b)
    assert _pair_ids(result) == {("teak", "right")}
    assert result.unmatched_b == ["near"]


def test_benchmark_zigzag_recovers_shifted_noisy_session() -> None:
    session_a, session_b, truth = build_sessions()
    result = MatchEngine().match(session_a, session_b)
    predicted = [(str(item.id_a), str(item.id_b)) for item in result.matches]
    precision, recall = score(predicted, truth)
    assert precision == 1.0
    assert recall == 1.0
    assert result.translation_east_m == pytest.approx(11.0, abs=2.0)
    assert result.translation_north_m == pytest.approx(-6.0, abs=2.0)
