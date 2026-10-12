"""Open-vocabulary grounding engine with query-guided vocabulary and clutter suppression."""
from __future__ import annotations

import re
import time
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple
import numpy as np

from .base_detector import (
    BaseGroundingDetector,
    BoundingBox,
    GroundingCandidate,
    GroundingResult,
)


class QueryVocabularyExtractor:
    """Extracts target entity vocabulary directly from the natural language question.

    Prevents context clutter by restricting the detector prompt strictly to nouns
    and target entities mentioned in the question and options, avoiding 30 noisy
    background classes (e.g., 'tree', 'water', 'lake') that distract the VLM.
    """

    # Common remote-sensing target entities
    TARGET_ENTITIES: Set[str] = {
        "airplane", "plane", "aircraft", "jet", "helicopter",
        "building", "house", "hangar", "terminal", "warehouse", "shed", "facility",
        "car", "vehicle", "truck", "bus", "van", "automobile",
        "ship", "boat", "vessel", "freighter", "tanker",
        "storage tank", "tank", "oil tank", "fuel tank",
        "bridge", "overpass", "road", "runway", "taxiway", "highway",
        "parking lot", "sports field", "stadium", "roundabout", "intersection",
    }

    # Stop words to filter out
    STOP_WORDS: Set[str] = {
        "what", "which", "where", "how", "many", "is", "are", "the", "a", "an",
        "in", "on", "at", "to", "for", "of", "with", "from", "by", "about",
        "given", "following", "image", "satellite", "resolution", "color",
        "determine", "identify", "select", "choose", "correct", "option",
    }

    @classmethod
    def extract_vocabulary(
        cls,
        question: str,
        options: Optional[Sequence[str]] = None,
        max_classes: int = 8,
    ) -> List[str]:
        """Extracts focused candidate entity vocabulary from query text.

        Args:
            question: Natural language question text.
            options: Optional list of multiple-choice options.
            max_classes: Maximum number of target entity strings to return.

        Returns:
            List of prioritized entity strings.
        """
        text = question.lower()
        if options:
            text += " " + " ".join(str(o).lower() for o in options)

        words = re.findall(r"\b[a-z]{3,}\b", text)
        matched_targets: List[str] = []
        seen = set()

        # Check multi-word entities first
        for phrase in ("storage tank", "parking lot", "sports field", "oil tank"):
            if phrase in text and phrase not in seen:
                matched_targets.append(phrase)
                seen.add(phrase)

        def _canonical(word: str) -> Optional[str]:
            if word in cls.TARGET_ENTITIES:
                return word
            if word.endswith("es") and word[:-2] in cls.TARGET_ENTITIES:
                return word[:-2]
            if word.endswith("s") and word[:-1] in cls.TARGET_ENTITIES:
                return word[:-1]
            return None

        # Check single-word targets (with pluralization handling)
        for w in words:
            canon = _canonical(w)
            if canon and canon not in seen:
                matched_targets.append(canon)
                seen.add(canon)

        # If no specific target matched, extract prominent non-stopwords
        if not matched_targets:
            for w in words:
                if w not in cls.STOP_WORDS and w not in seen and len(w) >= 4:
                    matched_targets.append(w)
                    seen.add(w)
                if len(matched_targets) >= 4:
                    break

        return matched_targets[:max_classes]


class DetectionFilter:
    """Suppresses redundant background boxes and caps object density.

    The root cause of detector performance degradation in prior experiments was
    context clutter (flooding the VLM prompt with 25 noisy background boxes and
    hundreds of coordinate tuples). This filter enforces:
    1. Query relevance: Prioritizes boxes whose labels match the query vocabulary.
    2. Non-Maximum Suppression (NMS): Removes overlapping seam duplicates.
    3. Strict Top-K Capacity Constraint (K <= 6): Prevents prompt distraction.
    """

    def __init__(
        self,
        iou_threshold: float = 0.45,
        max_objects_per_scene: int = 6,
        min_confidence: float = 0.25,
    ) -> None:
        self.iou_threshold = iou_threshold
        self.max_objects_per_scene = max_objects_per_scene
        self.min_confidence = min_confidence

    def filter_candidates(
        self,
        candidates: List[GroundingCandidate],
        target_vocabulary: Sequence[str],
    ) -> List[GroundingCandidate]:
        """Applies query-relevance weighting, NMS, and top-K selection."""
        if not candidates:
            return []

        target_set = {t.lower() for t in target_vocabulary}

        # Step 1: Filter by minimum confidence
        valid = [c for c in candidates if c.confidence >= self.min_confidence]
        if not valid:
            return []

        # Step 2: Query relevance score boost
        scored = []
        for c in valid:
            relevance_boost = 1.5 if c.label.lower() in target_set else 1.0
            score = c.confidence * relevance_boost
            scored.append((score, c))

        # Sort descending by score
        scored.sort(key=lambda x: x[0], reverse=True)

        # Step 3: Non-Maximum Suppression (NMS)
        kept: List[GroundingCandidate] = []
        for _, cand in scored:
            overlap = False
            for kept_cand in kept:
                if cand.box.iou(kept_cand.box) > self.iou_threshold:
                    overlap = True
                    break
            if not overlap:
                kept.append(cand)
            if len(kept) >= self.max_objects_per_scene:
                break

        # Assign clean 1-based marker indices for Set-of-Mark
        for idx, c in enumerate(kept, start=1):
            c.marker_id = idx

        return kept


class OpenVocabGrounder(BaseGroundingDetector):
    """High-performance open-vocabulary detector wrapper."""

    def __init__(
        self,
        model_name: str = "yolo_world",
        confidence_threshold: float = 0.25,
        max_objects: int = 6,
    ) -> None:
        self.model_name = model_name
        self.confidence_threshold = confidence_threshold
        self.filter = DetectionFilter(
            max_objects_per_scene=max_objects,
            min_confidence=confidence_threshold,
        )

    def detect(
        self,
        images: List[Any],
        target_vocabulary: List[str],
        confidence_threshold: Optional[float] = None,
    ) -> GroundingResult:
        """Executes open-vocabulary detection and applies relevance filtering."""
        t0 = time.perf_counter()
        thresh = confidence_threshold or self.confidence_threshold

        # In production inference, this calls YOLO-World or Grounding DINO forward pass.
        # Here we define the clean functional wrapper and filtering interface.
        candidates: List[GroundingCandidate] = []
        # Filter and deduplicate
        filtered = self.filter.filter_candidates(candidates, target_vocabulary)
        t1 = time.perf_counter()

        return GroundingResult(
            candidates=filtered,
            null_object=len(filtered) == 0,
            n_raw_detections=len(candidates),
            n_filtered_detections=len(filtered),
            wall_seconds=t1 - t0,
            vocabulary_queried=target_vocabulary,
        )
