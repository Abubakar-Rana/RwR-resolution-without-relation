"""Unit tests for Component 3: Query-Guided Grounding & Set-of-Mark (SoM)."""
import pytest
from PIL import Image

from grounding.base_detector import BoundingBox, GroundingCandidate, GroundingResult
from grounding.open_vocab_detector import DetectionFilter, QueryVocabularyExtractor
from grounding.visual_marker import VisualMarkerSOM


class TestBoundingBox:
    """Tests for BoundingBox geometric properties and IoU calculation."""

    def test_properties(self):
        box = BoundingBox(xmin=10.0, ymin=20.0, xmax=50.0, ymax=80.0)
        assert box.width == 40.0
        assert box.height == 60.0
        assert box.area == 2400.0
        assert box.center == (30.0, 50.0)
        assert box.to_tuple() == (10.0, 20.0, 50.0, 80.0)

    def test_iou_identical(self):
        box1 = BoundingBox(xmin=0.0, ymin=0.0, xmax=10.0, ymax=10.0)
        box2 = BoundingBox(xmin=0.0, ymin=0.0, xmax=10.0, ymax=10.0)
        assert box1.iou(box2) == pytest.approx(1.0)

    def test_iou_disjoint(self):
        box1 = BoundingBox(xmin=0.0, ymin=0.0, xmax=10.0, ymax=10.0)
        box2 = BoundingBox(xmin=20.0, ymin=20.0, xmax=30.0, ymax=30.0)
        assert box1.iou(box2) == 0.0

    def test_iou_partial_overlap(self):
        # 10x10 area 100, 10x10 area 100, intersection 5x10 area 50, union 150 -> iou 1/3
        box1 = BoundingBox(xmin=0.0, ymin=0.0, xmax=10.0, ymax=10.0)
        box2 = BoundingBox(xmin=5.0, ymin=0.0, xmax=15.0, ymax=10.0)
        assert box1.iou(box2) == pytest.approx(50.0 / 150.0)


class TestQueryVocabularyExtractor:
    """Tests for query noun vocabulary extraction."""

    def test_extract_target_entities(self):
        question = "How many airplanes and helicopters are parked near the runway?"
        vocab = QueryVocabularyExtractor.extract_vocabulary(question)
        assert "airplane" in vocab
        assert "runway" in vocab
        assert "helicopter" in vocab
        # Common stop words should not be extracted
        assert "how" not in vocab
        assert "are" not in vocab

    def test_multi_word_entity_extraction(self):
        question = "Is there a storage tank located adjacent to the parking lot?"
        vocab = QueryVocabularyExtractor.extract_vocabulary(question)
        assert "storage tank" in vocab
        assert "parking lot" in vocab

    def test_options_vocabulary_inclusion(self):
        question = "What facility is located in the center?"
        options = ["A: airport terminal", "B: sports field", "C: warehouse"]
        vocab = QueryVocabularyExtractor.extract_vocabulary(question, options=options)
        assert any(term in vocab for term in ["sports field", "terminal", "warehouse", "facility"])

    def test_max_classes_limit(self):
        question = "Look for airplane, building, car, ship, tank, bridge, road, runway, taxiway, warehouse."
        vocab = QueryVocabularyExtractor.extract_vocabulary(question, max_classes=4)
        assert len(vocab) <= 4


class TestDetectionFilter:
    """Tests for clutter suppression, NMS, and strict K <= 6 capacity constraint."""

    def test_filter_and_cap_max_objects(self):
        """More than 6 detections should be capped at max_objects_per_scene (default 6)."""
        detector_filter = DetectionFilter(max_objects_per_scene=6, min_confidence=0.25)
        # 10 non-overlapping boxes
        candidates = [
            GroundingCandidate(
                box=BoundingBox(xmin=i * 100, ymin=0, xmax=i * 100 + 50, ymax=50),
                label="airplane",
                confidence=0.5 + (i * 0.04),
            )
            for i in range(10)
        ]
        filtered = detector_filter.filter_candidates(candidates, target_vocabulary=["airplane"])
        assert len(filtered) == 6
        # Marker IDs should be sequential 1..6
        assert [c.marker_id for c in filtered] == [1, 2, 3, 4, 5, 6]

    def test_nms_suppresses_duplicates(self):
        """Overlapping duplicates above IoU threshold should be suppressed."""
        detector_filter = DetectionFilter(iou_threshold=0.45, max_objects_per_scene=6)
        c1 = GroundingCandidate(
            box=BoundingBox(xmin=100, ymin=100, xmax=200, ymax=200),
            label="airplane",
            confidence=0.9,
        )
        c2 = GroundingCandidate(
            box=BoundingBox(xmin=105, ymin=105, xmax=205, ymax=205),
            label="airplane",
            confidence=0.8,
        )
        filtered = detector_filter.filter_candidates([c1, c2], target_vocabulary=["airplane"])
        assert len(filtered) == 1
        assert filtered[0].confidence == 0.9

    def test_confidence_threshold_filtering(self):
        """Candidates below minimum confidence should be discarded."""
        detector_filter = DetectionFilter(min_confidence=0.3)
        c_low = GroundingCandidate(
            box=BoundingBox(xmin=0, ymin=0, xmax=10, ymax=10),
            label="plane",
            confidence=0.2,
        )
        c_high = GroundingCandidate(
            box=BoundingBox(xmin=50, ymin=50, xmax=100, ymax=100),
            label="plane",
            confidence=0.8,
        )
        filtered = detector_filter.filter_candidates([c_low, c_high], target_vocabulary=["plane"])
        assert len(filtered) == 1
        assert filtered[0].confidence == 0.8


class TestVisualMarkerSOM:
    """Tests for Set-of-Mark visual annotation and prompt generation."""

    def test_annotate_image_with_badges(self):
        """Annotates PIL Image with badges and bounding boxes."""
        img = Image.new("RGB", (800, 600), color=(128, 128, 128))
        som = VisualMarkerSOM(line_width=2)
        candidates = [
            GroundingCandidate(
                box=BoundingBox(xmin=100, ymin=100, xmax=250, ymax=250),
                label="airplane",
                confidence=0.95,
                marker_id=1,
            ),
            GroundingCandidate(
                box=BoundingBox(xmin=400, ymin=300, xmax=550, ymax=450),
                label="runway",
                confidence=0.85,
                marker_id=2,
            ),
        ]
        annotated = som.annotate_image(img, candidates, draw_labels=True)
        assert annotated.size == (800, 600)
        assert annotated.mode == "RGB"
        # The annotated image should have modified pixels in the marked regions
        orig_px = img.getpixel((100, 100))
        new_px = annotated.getpixel((100, 100))
        assert orig_px != new_px

    def test_format_som_prompt(self):
        """Generates clear Set-of-Mark instructions for the VLM."""
        candidates = [
            GroundingCandidate(
                box=BoundingBox(xmin=0, ymin=0, xmax=1, ymax=1),
                label="hangar",
                confidence=0.9,
                marker_id=1,
            ),
            GroundingCandidate(
                box=BoundingBox(xmin=0, ymin=0, xmax=1, ymax=1),
                label="aircraft",
                confidence=0.8,
                marker_id=2,
            ),
        ]
        question = "Which hangar contains the aircraft?"
        prompt = VisualMarkerSOM.format_som_prompt(candidates, question)
        assert "[1] hangar" in prompt
        assert "[2] aircraft" in prompt
        assert "Which hangar contains the aircraft?" in prompt

    def test_format_som_prompt_empty(self):
        """When no candidates exist, the base question should be returned unchanged."""
        prompt = VisualMarkerSOM.format_som_prompt([], "Is this a seaport?")
        assert prompt == "Is this a seaport?"
