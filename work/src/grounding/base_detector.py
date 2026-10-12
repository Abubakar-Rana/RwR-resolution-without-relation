"""Base interfaces and data structures for open-vocabulary visual grounding."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
import numpy as np


@dataclass
class BoundingBox:
    """Represents an axis-aligned bounding box in normalized or pixel coordinates."""
    xmin: float
    ymin: float
    xmax: float
    ymax: float

    @property
    def width(self) -> float:
        return max(0.0, self.xmax - self.xmin)

    @property
    def height(self) -> float:
        return max(0.0, self.ymax - self.ymin)

    @property
    def area(self) -> float:
        return self.width * self.height

    @property
    def center(self) -> Tuple[float, float]:
        return ((self.xmin + self.xmax) / 2.0, (self.ymin + self.ymax) / 2.0)

    def to_tuple(self) -> Tuple[float, float, float, float]:
        return (self.xmin, self.ymin, self.xmax, self.ymax)

    def iou(self, other: BoundingBox) -> float:
        """Calculates Intersection over Union (IoU) with another box."""
        ixmin = max(self.xmin, other.xmin)
        iymin = max(self.ymin, other.ymin)
        ixmax = min(self.xmax, other.xmax)
        iymax = min(self.ymax, other.ymax)
        iw = max(0.0, ixmax - ixmin)
        ih = max(0.0, iymax - iymin)
        inter = iw * ih
        union = self.area + other.area - inter
        return inter / union if union > 0 else 0.0


@dataclass
class GroundingCandidate:
    """Represents a detected object candidate."""
    box: BoundingBox
    label: str
    confidence: float
    tile_index: int = 0
    global_box: Optional[BoundingBox] = None
    marker_id: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GroundingResult:
    """Result of grounding detection across a scene or tile set."""
    candidates: List[GroundingCandidate] = field(default_factory=list)
    null_object: bool = True
    n_raw_detections: int = 0
    n_filtered_detections: int = 0
    wall_seconds: float = 0.0
    vocabulary_queried: List[str] = field(default_factory=list)

    @property
    def count(self) -> int:
        return len(self.candidates)


class BaseGroundingDetector(ABC):
    """Abstract interface for open-vocabulary object detectors."""

    @abstractmethod
    def detect(
        self,
        images: List[Any],
        target_vocabulary: List[str],
        confidence_threshold: float = 0.25,
    ) -> GroundingResult:
        """Runs open-vocabulary detection on images against target vocabulary."""
        raise NotImplementedError
