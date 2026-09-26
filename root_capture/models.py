"""Records for root-capture classification."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class PointLocation:
    """WGS84 position. ``lon`` is x, ``lat`` is y."""

    lon: float
    lat: float


@dataclass
class SessionSegment:
    """One walk whose footprint is the convex hull of its capture points."""

    id: str
    start_time: datetime
    points: List[PointLocation] = field(default_factory=list)


@dataclass
class Capture:
    """A single tree capture that may be an original planting or a re-visit."""

    id: str
    session_segment_id: str
    location: PointLocation
    timestamp: datetime
    root: Optional[bool] = None
