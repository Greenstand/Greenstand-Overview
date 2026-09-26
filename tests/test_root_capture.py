"""Tests for root-capture classification against session convex hulls."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from root_capture.models import Capture, PointLocation, SessionSegment
from root_capture.processor import RootCaptureProcessor

T0 = datetime(2023, 6, 1, 8, 0, tzinfo=timezone.utc)


def _at(lon: float, lat: float) -> PointLocation:
    return PointLocation(lon=lon, lat=lat)


def _session(session_id: str, hour: int, points: list[tuple[float, float]]) -> SessionSegment:
    return SessionSegment(
        id=session_id,
        start_time=T0 + timedelta(hours=hour),
        points=[_at(lon, lat) for lon, lat in points],
    )


def _capture(capture_id: str, session_id: str, lon: float, lat: float, minute: int = 0) -> Capture:
    return Capture(
        id=capture_id,
        session_segment_id=session_id,
        location=_at(lon, lat),
        timestamp=T0 + timedelta(minutes=minute),
    )


def _square(origin_lon: float, origin_lat: float, size: float = 0.01) -> list[tuple[float, float]]:
    return [
        (origin_lon, origin_lat),
        (origin_lon + size, origin_lat),
        (origin_lon + size, origin_lat + size),
        (origin_lon, origin_lat + size),
    ]


def test_overlapping_sessions_keep_only_the_earliest_as_root() -> None:
    # Three walks over the same square, t1 < t2 < t3.
    square = _square(10.0, 20.0)
    sessions = [
        _session("s1", 1, square),
        _session("s2", 2, [(10.002, 20.002), (10.004, 20.002), (10.003, 20.006)]),
        _session("s3", 3, [(10.005, 20.003), (10.007, 20.004), (10.006, 20.008)]),
    ]
    captures = [
        _capture("c1", "s1", 10.005, 20.005),
        _capture("c2", "s2", 10.003, 20.004),
        _capture("c3", "s3", 10.006, 20.005),
        # Later session, but this point is outside the first planting.
        _capture("c2-out", "s2", 10.05, 20.05),
    ]
    # Give the outside capture its own hull by adding those points to s2.
    sessions[1].points.append(_at(10.05, 20.05))
    sessions[1].points.append(_at(10.052, 20.05))
    sessions[1].points.append(_at(10.051, 20.053))

    result = RootCaptureProcessor().process_captures(captures, sessions)
    flags = {item.id: item.root for item in result}
    assert flags == {"c1": True, "c2": False, "c3": False, "c2-out": True}


def test_disjoint_sessions_are_all_roots() -> None:
    sessions = [
        _session("west", 1, _square(0.0, 0.0)),
        _session("east", 5, _square(1.0, 0.0)),
    ]
    captures = [
        _capture("w", "west", 0.005, 0.005),
        _capture("e", "east", 1.005, 0.005),
    ]
    result = RootCaptureProcessor().process_captures(captures, sessions)
    assert [item.root for item in result] == [True, True]


def test_single_point_collinear_and_boundary() -> None:
    processor = RootCaptureProcessor(buffer_meters=1.5)
    sessions = [
        _session("dot", 1, [(30.0, 1.0)]),
        _session("line", 2, [(31.0, 1.0), (31.0, 1.001)]),
        _session("pad", 3, _square(32.0, 1.0)),
    ]
    # Midpoint of the two-point walk, and both endpoints.
    captures = [
        _capture("on-dot", "dot", 30.0, 1.0),
        _capture("line-start", "line", 31.0, 1.0),
        _capture("line-mid", "line", 31.0, 1.0005),
        _capture("line-end", "line", 31.0, 1.001),
        _capture("vertex", "pad", 32.0, 1.0),
    ]
    # A later walk. The capture itself sits on pad's corner, not inside "later".
    sessions.append(_session("later", 4, _square(40.0, 1.0)))
    captures.append(_capture("revisit-vertex", "later", 32.0, 1.0))
    result = processor.process_captures(captures, sessions)
    flags = {item.id: item.root for item in result}
    assert flags["on-dot"] is True
    assert flags["line-start"] is True
    assert flags["line-mid"] is True
    assert flags["line-end"] is True
    assert flags["vertex"] is True
    assert flags["revisit-vertex"] is False


def test_capture_outside_every_hull_is_root() -> None:
    sessions = [_session("s", 1, _square(0.0, 0.0))]
    captures = [_capture("away", "s", 5.0, 5.0)]
    result = RootCaptureProcessor().process_captures(captures, sessions)
    assert result[0].root is True


def test_empty_inputs_and_duplicate_session_id() -> None:
    processor = RootCaptureProcessor()
    assert processor.process_captures([], []) == []
    lonely = _capture("x", "missing", 0.0, 0.0)
    processor.process_captures([lonely], [])
    assert lonely.root is True
    with pytest.raises(ValueError, match="duplicate"):
        processor.process_captures(
            [],
            [
                _session("same", 1, _square(0.0, 0.0)),
                _session("same", 2, _square(1.0, 1.0)),
            ],
        )


def test_strtree_query_on_a_hundred_sessions() -> None:
    sessions: list[SessionSegment] = []
    captures: list[Capture] = []
    for i in range(100):
        origin = i * 0.05
        sessions.append(_session(f"s{i}", i, _square(origin, 0.0, size=0.01)))
        for k in range(10):
            captures.append(
                _capture(
                    f"c{i}-{k}",
                    f"s{i}",
                    origin + 0.002 + k * 0.0005,
                    0.002 + (k % 3) * 0.002,
                    minute=k,
                )
            )
    # One later session planted on top of session 0. Those captures are re-tracks.
    sessions.append(_session("revisit", 500, _square(0.0, 0.0, size=0.008)))
    captures.append(_capture("again", "revisit", 0.004, 0.004))

    result = RootCaptureProcessor().process_captures(captures, sessions)
    assert len(result) == 1001
    flags = {item.id: item.root for item in result}
    assert flags["again"] is False
    assert all(flags[f"c{i}-{k}"] is True for i in range(100) for k in range(10))
    assert all(item.root is not None for item in result)
