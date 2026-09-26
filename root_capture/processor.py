"""Classify captures as root plantings or re-tracks.

A session segment is the convex hull of the points collected on one walk.
A capture is a root capture when its own session is the earliest session
whose hull covers that location. If an older hull also covers it, the
capture is a re-track of that earlier planting.

Hulls are stored in an STRtree so each capture queries candidates in
logarithmic time instead of scanning every session.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List

from shapely import STRtree
from shapely.geometry import MultiPoint, Point
from shapely.geometry.base import BaseGeometry

from root_capture.models import Capture, SessionSegment

METERS_PER_DEGREE = 111_320.0


@dataclass(frozen=True)
class _IndexedSession:
    id: str
    start_time: datetime
    hull: BaseGeometry


class RootCaptureProcessor:
    """Assign ``Capture.root`` from session convex hulls.

    Parameters
    ----------
    buffer_meters:
        Radius used when a session has fewer than three non-collinear
        points. The hull is then a line or a point, which cannot contain
        anything, so it is expanded by this distance before indexing.
    """

    def __init__(self, buffer_meters: float = 1.5) -> None:
        if buffer_meters <= 0:
            raise ValueError("buffer_meters must be positive")
        self.buffer_meters = buffer_meters

    def process_captures(
        self,
        captures: List[Capture],
        sessions: List[SessionSegment],
    ) -> List[Capture]:
        """Set ``root`` on each capture and return the same list.

        A capture covered by no hull is treated as a root capture: it is
        not a re-track of any known planting. When several hulls share the
        earliest start time, the capture is a root if its session is one
        of those sessions.
        """
        indexed = self._index_sessions(sessions)
        if not indexed:
            for capture in captures:
                capture.root = True
            return captures

        tree = STRtree([item.hull for item in indexed])
        for capture in captures:
            point = Point(capture.location.lon, capture.location.lat)
            # Shapely calls predicate(query, indexed). covered_by keeps
            # boundary points, which contains/within would drop.
            hits = tree.query(point, predicate="covered_by")
            if len(hits) == 0:
                capture.root = True
                continue
            earliest = min(indexed[int(i)].start_time for i in hits)
            earliest_ids = {
                indexed[int(i)].id
                for i in hits
                if indexed[int(i)].start_time == earliest
            }
            capture.root = capture.session_segment_id in earliest_ids
        return captures

    def _index_sessions(self, sessions: List[SessionSegment]) -> List[_IndexedSession]:
        indexed: list[_IndexedSession] = []
        seen: set[str] = set()
        for session in sessions:
            if session.id in seen:
                raise ValueError(f"duplicate session segment id: {session.id}")
            seen.add(session.id)
            hull = self._hull(session)
            if hull is None:
                continue
            indexed.append(_IndexedSession(session.id, session.start_time, hull))
        return indexed

    def _hull(self, session: SessionSegment) -> BaseGeometry | None:
        if not session.points:
            return None
        coords = [(point.lon, point.lat) for point in session.points]
        hull = MultiPoint(coords).convex_hull
        if hull.is_empty:
            return None
        # A point or a collinear run has no area. Buffer it so a capture
        # sitting on the walk still intersects the session.
        if hull.geom_type != "Polygon" or hull.area == 0:
            eps = self.buffer_meters / METERS_PER_DEGREE
            hull = hull.buffer(eps)
        if hull.is_empty:
            return None
        return hull
