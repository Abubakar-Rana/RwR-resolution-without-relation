"""Adversarial stress test suite for Grounded Dual-Scale Pyramid Architecture.

Empirically challenges all 7 core components with extreme boundary conditions:
- Smart padding under extreme aspect ratios (100:1, 1:100, 1x8500, 8500x1) and out-of-bounds boxes.
- Quad-tree seam severance boundaries (exact center straddling, oversize objects, border cases).
- Continuous Global 2D-RoPE under out-of-bounds coordinates ([-1, 2], zero-width) and odd resolutions.
- Token compression under odd/prime spatial resolutions (1x17, 7x7, 13x13, 15x23).
- Prior and cascaded routers under adversarial task names, empty queries, and extreme thresholds.
- Dual-scale cross-attention under asymmetric sequences, extreme gate initializations, and high load.
- End-to-end pipeline robustness under malformed or adversarial inputs.
"""
from __future__ import annotations

import math
import numpy as np
import pytest
import torch
from PIL import Image

from active_search.quad_tree import HierarchicalQuadTree, QuadrantNode
from data.smart_padding import PaddingMetadata, SmartPaddingTransform
from geometry.global_2d_rope import ContinuousGlobal2DRoPE
from grounding.base_detector import BoundingBox, GroundingCandidate, GroundingResult
from grounding.open_vocab_detector import DetectionFilter, OpenVocabGrounder, QueryVocabularyExtractor
from grounding.visual_marker import VisualMarkerSOM
from models.grounded_pyramid_pipeline import GroundedDualScalePyramid, GroundedPyramidPipelineConfig
from models.pyramid_fusion import DualScalePyramidAggregator, PyramidalFusionConfig, SpatialCrossAttention
from models.token_compression import AdaptiveTokenPruner, PixelShuffleTokenCompressor
from routing.cascaded_router import CascadedHeuristicRouter, ParetoCalibratedRouter
from routing.prior_router import GroupPriorRouter, TaskEmpiricalRouter


# ==============================================================================
# 1. SMART PADDING ADVERSARIAL STRESS TESTS
# ==============================================================================
class TestSmartPaddingAdversarial:
    """Stress tests for Aspect-Ratio Preserving Smart Padding."""

    @pytest.mark.parametrize(
        "orig_size, target_size",
        [
            ((8500, 85), 1024),       # 100:1 extreme landscape
            ((85, 8500), 1024),       # 1:100 extreme portrait
            ((8500, 1), 1024),        # 1-pixel height extreme strip
            ((1, 8500), 1024),        # 1-pixel width extreme strip
            ((1, 1), 1024),           # Single pixel image
            ((10000, 10), 1024),      # 1000:1 ratio
            ((1024, 1024), (512, 1024)),  # Non-square target size (portrait)
            ((1024, 1024), (1024, 512)),  # Non-square target size (landscape)
            ((1500, 1500), (1023, 1023)), # Odd target dimension
        ],
    )
    def test_extreme_aspect_ratios_and_targets(self, orig_size, target_size):
        """Image resizes to exact target size without crash or distortion."""
        img = Image.new("RGB", orig_size, color=(100, 150, 200))
        transform = SmartPaddingTransform(target_size=target_size)
        padded_img, meta = transform(img)

        expected_w, expected_h = (target_size, target_size) if isinstance(target_size, int) else target_size
        assert padded_img.size == (expected_w, expected_h)
        assert meta.original_size == orig_size
        assert meta.target_size == (expected_w, expected_h)
        assert meta.pad_left >= 0 and meta.pad_top >= 0
        assert meta.pad_right >= 0 and meta.pad_bottom >= 0
        assert meta.pad_left + meta.resized_size[0] + meta.pad_right == expected_w
        assert meta.pad_top + meta.resized_size[1] + meta.pad_bottom == expected_h

    def test_reversibility_under_extreme_100_to_1_ratio(self):
        """Coordinate mapping roundtrip remains reversible even at 100:1 aspect ratio."""
        orig_w, orig_h = 8500, 85
        img = Image.new("RGB", (orig_w, orig_h), color=(0, 0, 0))
        transform = SmartPaddingTransform(target_size=1024)
        _, meta = transform(img)

        test_boxes = [
            (0.1, 0.2, 0.8, 0.9),
            (0.0, 0.0, 1.0, 1.0),
            (0.45, 0.1, 0.55, 0.9),
        ]
        for box in test_boxes:
            padded = transform.map_box_to_padded(box, meta, normalized_in=True, normalized_out=True)
            recovered = transform.map_box_from_padded(padded, meta, normalized_in=True, normalized_out=True)
            for orig_val, rec_val in zip(box, recovered):
                assert orig_val == pytest.approx(rec_val, abs=1e-3)

    def test_out_of_bounds_and_inverted_boxes(self):
        """Out-of-bounds coordinates clamp cleanly; inverted boxes do not crash."""
        meta = PaddingMetadata(
            original_size=(2000, 1000),
            target_size=(1024, 1024),
            resized_size=(1024, 512),
            scale_factor=0.512,
            pad_left=0,
            pad_top=256,
            pad_right=0,
            pad_bottom=256,
        )
        # Severe out-of-bounds: [-0.5, -0.5, 1.5, 1.5]
        recovered = SmartPaddingTransform.map_box_from_padded(
            (-0.5, -0.5, 1.5, 1.5), meta, normalized_in=True, normalized_out=True
        )
        assert recovered[0] == 0.0
        assert recovered[1] == 0.0
        assert recovered[2] == 1.0
        assert recovered[3] == 1.0

        # Zero-area box: [0.5, 0.5, 0.5, 0.5]
        padded_zero = SmartPaddingTransform.map_box_to_padded(
            (0.5, 0.5, 0.5, 0.5), meta, normalized_in=True, normalized_out=True
        )
        recovered_zero = SmartPaddingTransform.map_box_from_padded(
            padded_zero, meta, normalized_in=True, normalized_out=True
        )
        assert recovered_zero[0] == pytest.approx(0.5, abs=1e-3)
        assert recovered_zero[2] == pytest.approx(0.5, abs=1e-3)


# ==============================================================================
# 2. HIERARCHICAL QUAD-TREE ADVERSARIAL STRESS TESTS
# ==============================================================================
class TestHierarchicalQuadTreeAdversarial:
    """Stress tests for 15% Overlapped Hierarchical Quad-Tree Search."""

    @pytest.fixture
    def tree(self):
        return HierarchicalQuadTree(image_width=8500, image_height=8500, max_depth=2, overlap_ratio=0.15)

    def test_exact_quad_center_straddling_object(self, tree):
        """Object directly centered at the 4-quadrant junction (4250, 4250)."""
        # Object of size 200x200 centered at (4250, 4250)
        center_box = (4150, 4150, 4350, 4350)
        res = tree.check_object_severance(center_box, use_padded=True)

        # Unpadded cuts it horizontally AND vertically:
        assert res["severed_unpadded"] is True
        # 15% overlap expands each quadrant by 4250 * 0.15 = 637 pixels across the seam.
        # NW padded reaches x=4887, y=4887 (covers 4350, 4350).
        # Therefore, padded quadrant fully contains the object!
        assert res["severed_padded"] is False
        assert res["saved_by_padding"] is True

    def test_oversize_object_larger_than_overlap_margin(self, tree):
        """Object centered at (4250, 4250) but exceeding 2x the 15% overlap margin."""
        # Margin is 637 pixels on each side (total overlap width = 1274 px).
        # An object with width 2000 pixels (from 3250 to 5250) cannot fit in any single quadrant.
        huge_box = (3250, 3250, 5250, 5250)
        res = tree.check_object_severance(huge_box, use_padded=True)

        assert res["severed_unpadded"] is True
        # Cannot fit in a single padded quadrant:
        assert res["severed_padded"] is True
        assert res["saved_by_padding"] is False

    def test_mathematical_containment_threshold(self, tree):
        """Verify the exact mathematical boundary where 15% overlap can no longer contain a centered object."""
        # Quadrant L1 size is 4250. Overlap dx = 4250 * 0.15 = 637.
        # Padded NW extends to (4250 + 637) = 4887.
        # An object centered at 4250 with half-width <= 637 is contained.
        # Half-width = 630 -> width = 1260:
        box_fits = (4250 - 630, 4250 - 630, 4250 + 630, 4250 + 630)
        res_fits = tree.check_object_severance(box_fits, use_padded=True)
        assert res_fits["severed_padded"] is False

        # Half-width = 650 -> width = 1300 (> 637):
        box_exceeds = (4250 - 650, 4250 - 650, 4250 + 650, 4250 + 650)
        res_exceeds = tree.check_object_severance(box_exceeds, use_padded=True)
        assert res_exceeds["severed_padded"] is True

    def test_quadrant_scoring_stress_1000_boxes(self, tree):
        """Scoring 1,000 dense candidate boxes executes quickly without memory leaks."""
        np.random.seed(42)
        boxes = []
        for _ in range(1000):
            x = np.random.randint(0, 8000)
            y = np.random.randint(0, 8000)
            w = np.random.randint(50, 300)
            h = np.random.randint(50, 300)
            boxes.append((x, y, x + w, y + h))

        selected = tree.score_and_select_quadrants(boxes, max_crops=2)
        assert len(selected) == 2
        for s in selected:
            assert s.score > 0.0

    def test_adversarial_boxes_negative_and_zero_area(self, tree):
        """Degenerate target boxes (negative coordinates, zero area) degrade gracefully to ROOT."""
        bogus_boxes = [
            (-100, -100, -50, -50),
            (9000, 9000, 9500, 9500),
            (4000, 4000, 4000, 4000),  # zero area
        ]
        selected = tree.score_and_select_quadrants(bogus_boxes, max_crops=2)
        assert len(selected) == 1
        assert selected[0].quadrant_name == "ROOT"


# ==============================================================================
# 3. OPEN-VOCABULARY GROUNDING & SET-OF-MARK ADVERSARIAL STRESS TESTS
# ==============================================================================
class TestGroundingAdversarial:
    """Stress tests for Open-Vocabulary Grounding, Query Vocabulary, and Visual Markers."""

    @pytest.mark.parametrize(
        "query, expected_non_empty",
        [
            ("", False),
            ("     \t\n   ", False),
            ("!@#$%^&*()_+{}[]:;<>?,./~`", False),
            ("12345 67890 3.14159", False),
            ("SELECT * FROM images WHERE 1=1;", True),  # extracts 'select', 'images'
            ("How many aircraft and oil tanks are visible near the runways?", True),
        ],
    )
    def test_vocabulary_extractor_adversarial_queries(self, query, expected_non_empty):
        """QueryVocabularyExtractor handles empty, symbolic, or adversarial queries gracefully."""
        vocab = QueryVocabularyExtractor.extract_vocabulary(query)
        if expected_non_empty:
            assert len(vocab) > 0
        else:
            assert len(vocab) == 0

    def test_vocabulary_extractor_large_text(self):
        """QueryVocabularyExtractor caps vocabulary under 50KB question text."""
        long_query = "Where are the airplanes and runways? " * 2000
        vocab = QueryVocabularyExtractor.extract_vocabulary(long_query, max_classes=8)
        assert len(vocab) <= 8
        assert "airplane" in vocab
        assert "runway" in vocab

    def test_detection_filter_dense_duplicate_clustering(self):
        """DetectionFilter suppresses 500 duplicate candidate boxes at the exact same location."""
        det_filter = DetectionFilter(iou_threshold=0.45, max_objects_per_scene=6, min_confidence=0.25)
        # 500 identical boxes
        cands = [
            GroundingCandidate(
                box=BoundingBox(0.2, 0.2, 0.4, 0.4),
                label="airplane",
                confidence=0.5 + (i * 0.0005),
            )
            for i in range(500)
        ]
        filtered = det_filter.filter_candidates(cands, target_vocabulary=["airplane"])
        # All duplicates suppressed by NMS -> exactly 1 candidate kept
        assert len(filtered) == 1
        assert filtered[0].marker_id == 1

    def test_visual_marker_som_extreme_coordinates_and_empty(self):
        """VisualMarkerSOM annotates safely with empty or border-touching coordinates."""
        marker = VisualMarkerSOM()
        img = Image.new("RGB", (512, 512), color=(50, 50, 50))

        # Empty candidate list
        annotated_empty = marker.annotate_image(img, [])
        assert annotated_empty.size == (512, 512)

        # Border-touching and out-of-bounds candidates
        cands = [
            GroundingCandidate(box=BoundingBox(0.0, 0.0, 0.1, 0.1), label="nw_corner", confidence=0.9, marker_id=1),
            GroundingCandidate(box=BoundingBox(0.9, 0.9, 1.0, 1.0), label="se_corner", confidence=0.9, marker_id=2),
            GroundingCandidate(box=BoundingBox(-0.2, -0.2, 0.05, 0.05), label="clamped", confidence=0.9, marker_id=3),
        ]
        annotated = marker.annotate_image(img, cands)
        assert annotated.size == (512, 512)


# ==============================================================================
# 4. CONTINUOUS GLOBAL 2D-RoPE ADVERSARIAL STRESS TESTS
# ==============================================================================
class TestContinuousGlobal2DRoPEAdversarial:
    """Stress tests for Continuous Global 2D Rotary Position Embeddings."""

    @pytest.fixture
    def rope(self):
        return ContinuousGlobal2DRoPE(dim=64, theta=10000.0)

    @pytest.mark.parametrize(
        "bounds",
        [
            (-1.0, -1.0, 0.5, 0.5),      # Negative out-of-bounds coordinates
            (0.5, 0.5, 2.0, 2.0),       # High positive out-of-bounds coordinates
            (-2.0, -2.0, 3.0, 3.0),     # Massive bounding box
            (0.5, 0.5, 0.5, 0.5),       # Zero-width / zero-height degenerate bounds
            (0.8, 0.8, 0.2, 0.2),       # Inverted coordinates (u0 > u1, v0 > v1)
        ],
    )
    def test_out_of_bounds_and_inverted_coordinates(self, rope, bounds):
        """RoPE forward produces strictly bounded cos/sin in [-1.0, 1.0] and cos^2 + sin^2 == 1."""
        grid_h, grid_w = 8, 8
        cos, sin = rope(grid_h, grid_w, bounds)

        assert cos.shape == (64, 64)
        assert sin.shape == (64, 64)
        assert torch.all(cos >= -1.0 - 1e-6) and torch.all(cos <= 1.0 + 1e-6)
        assert torch.all(sin >= -1.0 - 1e-6) and torch.all(sin <= 1.0 + 1e-6)
        # Trigonometric identity check
        sq_sum = (cos ** 2) + (sin ** 2)
        assert torch.allclose(sq_sum, torch.ones_like(sq_sum), atol=1e-5)

    @pytest.mark.parametrize(
        "grid_h, grid_w",
        [
            (1, 1),      # 1x1 single token
            (1, 64),     # 1x64 highly rectangular line
            (64, 1),     # 64x1 vertical line
            (7, 11),     # Prime non-power-of-2 dimensions
            (13, 17),    # Odd spatial grid
        ],
    )
    def test_odd_and_asymmetric_spatial_grids(self, rope, grid_h, grid_w):
        """RoPE computes valid embeddings for non-square and prime spatial resolutions."""
        cos, sin = rope(grid_h, grid_w, (0.0, 0.0, 1.0, 1.0))
        expected_seq_len = grid_h * grid_w
        assert cos.shape == (expected_seq_len, 64)
        assert sin.shape == (expected_seq_len, 64)

    def test_apply_rope_2d_norm_invariance_adversarial(self, rope):
        """Unitary transformation: vector L2 norms are preserved under extreme coordinates."""
        B, num_heads, seq_len, head_dim = 2, 4, 32, 64
        x = torch.randn(B, num_heads, seq_len, head_dim)
        # Extreme coordinates
        cos, sin = rope(4, 8, (-5.0, -5.0, 10.0, 10.0))

        rotated = ContinuousGlobal2DRoPE.apply_rope_2d(x, cos, sin)
        norm_orig = torch.norm(x, dim=-1)
        norm_rot = torch.norm(rotated, dim=-1)
        assert torch.allclose(norm_orig, norm_rot, atol=1e-4)


# ==============================================================================
# 5. TOKEN COMPRESSION ADVERSARIAL STRESS TESTS
# ==============================================================================
class TestTokenCompressionAdversarial:
    """Stress tests for Pixel-Shuffle 2x2 Token Compression and Adaptive Pruning."""

    @pytest.fixture
    def compressor(self):
        return PixelShuffleTokenCompressor(in_dim=128, out_dim=256, scale_factor=2)

    @pytest.mark.parametrize(
        "H, W, expected_new_H, expected_new_W",
        [
            (1, 1, 1, 1),     # 1x1 padded to 2x2 -> compressed to 1x1
            (1, 17, 1, 9),    # Odd width: 17 padded to 18 -> 9
            (7, 7, 4, 4),     # 7x7 padded to 8x8 -> compressed to 4x4
            (13, 13, 7, 7),   # 13x13 padded to 14x14 -> compressed to 7x7
            (15, 23, 8, 12),  # Asymmetric odd: 15->16 (8), 23->24 (12)
            (3, 5, 2, 3),     # 3->4 (2), 5->6 (3)
        ],
    )
    def test_odd_and_prime_spatial_shapes_compression(self, compressor, H, W, expected_new_H, expected_new_W):
        """Replicate padding smoothly handles odd and prime spatial resolutions."""
        B, D = 1, 128
        x = torch.randn(B, H, W, D)
        out, (new_h, new_w) = compressor(x)

        assert new_h == expected_new_H
        assert new_w == expected_new_W
        assert out.shape == (B, expected_new_H * expected_new_W, 256)

    def test_non_square_sequence_length_rejection(self, compressor):
        """Flattened 3D input with non-square N raises clear ValueError when spatial_shape is omitted."""
        B, N, D = 1, 17, 128  # 17 is prime
        x = torch.randn(B, N, D)
        with pytest.raises(ValueError, match="Cannot infer square spatial shape"):
            compressor(x)

    def test_explicit_spatial_shape_with_prime_factors(self, compressor):
        """Passing explicit rectangular spatial_shape for non-square N works smoothly."""
        B, D = 1, 128
        H, W = 5, 7  # N = 35
        x = torch.randn(B, H * W, D)
        out, (new_h, new_w) = compressor(x, spatial_shape=(H, W))

        # 5 padded to 6 -> 3, 7 padded to 8 -> 4
        assert new_h == 3
        assert new_w == 4
        assert out.shape == (B, 12, 256)

    def test_adaptive_pruner_boundary_ratios(self):
        """AdaptiveTokenPruner handles keep_ratio=1.0 and keep_ratio=0.0 gracefully."""
        B, N, D = 2, 20, 64
        x = torch.randn(B, N, D)
        salience = torch.rand(B, N)

        # 100% keep
        pruner_full = AdaptiveTokenPruner(keep_ratio=1.0)
        out_full = pruner_full(x, salience)
        assert out_full.shape == (B, 20, D)

        # 0.0 keep should clamp to minimum 1 token
        pruner_zero = AdaptiveTokenPruner(keep_ratio=0.0)
        out_zero = pruner_zero(x, salience)
        assert out_zero.shape == (B, 1, D)


# ==============================================================================
# 6. DUAL-SCALE PYRAMIDAL FUSION ADVERSARIAL STRESS TESTS
# ==============================================================================
class TestPyramidFusionAdversarial:
    """Stress tests for Dual-Scale Cross-Attention Pyramidal Aggregator."""

    @pytest.fixture
    def aggregator(self):
        cfg = PyramidalFusionConfig(
            hidden_dim=128,
            num_heads=4,
            dropout=0.0,
            gate_init=0.0,
            rope_dim=32,
        )
        return DualScalePyramidAggregator(cfg)

    def test_fuse_crop_explicit_rectangular_grid(self, aggregator):
        """Fuses rectangular crop tokens with explicit (grid_h, grid_w)."""
        B, D = 1, 128
        # Rectangular crop tokens: 4 x 8 = 32
        loc_tokens = torch.randn(B, 32, D)
        glob_tokens = torch.randn(B, 64, D)  # 8 x 8 = 64
        crop_bounds = (0.1, 0.2, 0.6, 0.7)

        fused = aggregator.fuse_crop_with_overview(
            local_crop_tokens=loc_tokens,
            global_overview_tokens=glob_tokens,
            crop_norm_bounds=crop_bounds,
            grid_h=4,
            grid_w=8,
        )
        assert fused.shape == (B, 32, D)

    def test_aggregate_multiscale_sequence_zero_crops(self, aggregator):
        """Zero crops simply returns the global overview tokens."""
        B, D = 1, 128
        glob_tokens = torch.randn(B, 64, D)

        out = aggregator.aggregate_multiscale_sequence(
            global_overview_tokens=glob_tokens,
            crop_tokens_list=[],
            crop_bounds_list=[],
            include_global_tokens=True,
        )
        assert out.shape == (B, 64, D)

    def test_aggregate_multiscale_sequence_10_crops_high_budget(self, aggregator):
        """Aggregating 10 crops scales cleanly without shape errors."""
        B, D = 1, 128
        glob_tokens = torch.randn(B, 64, D)
        crops = [torch.randn(B, 64, D) for _ in range(10)]
        bounds = [(0.0, 0.0, 0.5, 0.5)] * 10

        out = aggregator.aggregate_multiscale_sequence(
            global_overview_tokens=glob_tokens,
            crop_tokens_list=crops,
            crop_bounds_list=bounds,
            include_global_tokens=True,
        )
        # 64 global + 10 * 64 crops = 704 tokens
        assert out.shape == (B, 704, D)

    def test_extreme_gating_weights_stability(self):
        """Aggregator remains numerically stable under extreme gating initialization (+50, -50)."""
        B, D = 1, 128
        loc_tokens = torch.randn(B, 16, D)
        glob_tokens = torch.randn(B, 16, D)

        # Extreme positive gate (sigmoid -> 1.0)
        cfg_pos = PyramidalFusionConfig(hidden_dim=128, num_heads=4, gate_init=50.0, rope_dim=32)
        agg_pos = DualScalePyramidAggregator(cfg_pos)
        fused_pos = agg_pos.fuse_crop_with_overview(loc_tokens, glob_tokens, (0.0, 0.0, 0.5, 0.5))
        assert not torch.isnan(fused_pos).any()
        assert not torch.isinf(fused_pos).any()

        # Extreme negative gate (sigmoid -> 0.0, residual dominant)
        cfg_neg = PyramidalFusionConfig(hidden_dim=128, num_heads=4, gate_init=-50.0, rope_dim=32)
        agg_neg = DualScalePyramidAggregator(cfg_neg)
        fused_neg = agg_neg.fuse_crop_with_overview(loc_tokens, glob_tokens, (0.0, 0.0, 0.5, 0.5))
        assert not torch.isnan(fused_neg).any()
        assert not torch.isinf(fused_neg).any()


# ==============================================================================
# 7. ROUTING ADVERSARIAL STRESS TESTS
# ==============================================================================
class TestRoutersAdversarial:
    """Stress tests for Prior-based, Cascaded, and Pareto routers."""

    @pytest.mark.parametrize(
        "task_name, expected_route",
        [
            ("Object Spatial Relationship", "b1_direct"),
            ("Route Planning", "b1_direct"),
            ("Regional Counting", "b1_direct"),
            ("Counting with Complex Reasoning", "b1_direct"),
            ("Object Attribute", "b3_selected"),
            ("", "b3_selected"),                           # Empty string
            ("Unknown Mystery Task", "b3_selected"),       # Unseen task
            ("!@#$%^&*()", "b3_selected"),                 # Symbols
            ("object spatial relationship", "b3_selected"), # Lowercase (exact match required)
            ("A" * 10000, "b3_selected"),                  # Massive string
        ],
    )
    def test_group_prior_router_adversarial_queries(self, task_name, expected_route):
        """GroupPriorRouter returns safe deterministic routes for all inputs."""
        router = GroupPriorRouter()
        assert router.predict_single(task_name) == expected_route

    def test_task_empirical_router_unseen_task_fallback(self):
        """TaskEmpiricalRouter falls back safely when encountering unseen tasks."""
        router = TaskEmpiricalRouter()
        tasks = np.array(["TaskA", "TaskA", "TaskB", "TaskB"])
        correct = {
            "b1_direct": np.array([1, 1, 0, 0]),
            "b3_selected": np.array([0, 0, 1, 1]),
        }
        router.fit(tasks, correct, np.arange(4))

        assert router.predict_single("TaskA") == "b1_direct"
        assert router.predict_single("TaskB") == "b3_selected"
        # Unseen task falls back without crash
        assert router.predict_single("UnseenTask") in ("b1_direct", "b3_selected")

    @pytest.mark.parametrize("tau", [-0.5, 0.0, 0.5, 1.0, 1.5])
    def test_pareto_calibrated_router_extreme_thresholds(self, tau):
        """ParetoCalibratedRouter operates reliably across boundary thresholds."""
        router = ParetoCalibratedRouter(tau=tau)
        probs = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
        routes = router.predict_from_probabilities(probs)
        assert len(routes) == 5
        assert all(r in ("b1_direct", "b3_selected") for r in routes)


# ==============================================================================
# 8. INTEGRATED PIPELINE END-TO-END ADVERSARIAL STRESS TESTS
# ==============================================================================
class TestIntegratedPipelineAdversarial:
    """End-to-end stress tests on GroundedDualScalePyramid."""

    @pytest.fixture
    def pipeline(self):
        cfg = GroundedPyramidPipelineConfig(
            canvas_size=8500,
            quad_tree_overlap=0.15,
            max_active_crops=2,
            max_som_markers=6,
            hidden_dim=128,
            num_heads=4,
            rope_dim=32,
            enable_compression=True,
            enable_router_shortcircuit=True,
        )
        return GroundedDualScalePyramid(cfg)

    def test_process_scene_with_empty_and_corrupt_inputs(self, pipeline):
        """Pipeline processes scene smoothly with empty query, zero detections, and unknown task."""
        res = pipeline.process_scene_and_query(
            query_text="",
            task_name="Alien Invasion Scenario",
            detected_boxes=[],
        )
        assert res["route_decision"] == "b3_selected"
        assert res["short_circuit"] is False
        assert res["target_vocabulary"] == []
        assert res["n_grounded_boxes"] == 0
        assert res["selected_quadrants"] == ["ROOT"]
        assert res["n_vlm_forward_passes"] == 2

    def test_process_scene_with_excessive_boxes(self, pipeline):
        """Pipeline caps excessive candidate boxes to max_som_markers limit."""
        boxes = [(i * 100, i * 100, i * 100 + 50, i * 100 + 50) for i in range(50)]
        res = pipeline.process_scene_and_query(
            query_text="Find the buildings and runways",
            task_name="Object Attribute",
            detected_boxes=boxes,
        )
        assert res["n_grounded_boxes"] == pipeline.config.max_som_markers
        assert len(res["selected_quadrants"]) <= pipeline.config.max_active_crops

    def test_forward_tokens_with_uncompressed_and_compressed_streams(self, pipeline):
        """Multiscale token forward pass executes end-to-end with valid shapes."""
        B, N, D = 1, 64, 128  # 8x8 grid
        glob = torch.randn(B, N, D)
        crops = [torch.randn(B, N, D) for _ in range(2)]
        bounds = [(0.0, 0.0, 0.5, 0.5), (0.5, 0.5, 1.0, 1.0)]

        # With compression: 64 compresses to 16 tokens (4x4)
        fused = pipeline.forward_multiscale_tokens(glob, crops, bounds)
        # 16 global + 16 crop1 + 16 crop2 = 48 tokens
        assert fused.shape == (B, 48, D)
        assert not torch.isnan(fused).any()
