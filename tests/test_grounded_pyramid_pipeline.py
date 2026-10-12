"""Unit tests for the integrated GroundedDualScalePyramid pipeline."""
import pytest
import torch

from models.grounded_pyramid_pipeline import GroundedDualScalePyramid, GroundedPyramidPipelineConfig


class TestGroundedDualScalePyramid:
    """Tests for GroundedDualScalePyramid Grand Synthesis pipeline."""

    @pytest.fixture
    def pipeline(self):
        """Initializes pipeline with lightweight testing config."""
        config = GroundedPyramidPipelineConfig(
            canvas_size=8500,
            quad_tree_overlap=0.15,
            max_active_crops=2,
            max_som_markers=6,
            hidden_dim=256,
            num_heads=4,
            rope_dim=64,
            enable_compression=True,
            enable_router_shortcircuit=True,
        )
        return GroundedDualScalePyramid(config)

    def test_pipeline_initialization_components(self, pipeline):
        """All 7 components are properly initialized within the pipeline."""
        assert hasattr(pipeline, "quad_tree")
        assert hasattr(pipeline, "smart_padder")
        assert hasattr(pipeline, "rope_layer")
        assert hasattr(pipeline, "vocab_extractor")
        assert hasattr(pipeline, "det_filter")
        assert hasattr(pipeline, "visual_marker")
        assert hasattr(pipeline, "token_compressor")
        assert hasattr(pipeline, "pyramid_aggregator")
        assert hasattr(pipeline, "prior_router")

    def test_process_scene_relational_shortcircuit(self, pipeline):
        """Relational task should short-circuit to 1 VLM call via macro router."""
        result = pipeline.process_scene_and_query(
            query_text="What is the spatial relationship between the two airplanes?",
            task_name="Object Spatial Relationship",
            detected_boxes=[(1000, 1000, 1500, 1500), (4000, 4000, 4500, 4500)],
        )

        assert result["route_decision"] == "b1_direct"
        assert result["short_circuit"] is True
        assert result["n_vlm_forward_passes"] == 1
        assert "airplane" in result["target_vocabulary"]
        assert result["n_grounded_boxes"] == 2

    def test_process_scene_perceptual_multicrop(self, pipeline):
        """Fine-grained perceptual task must NOT short-circuit; executes quad-tree search."""
        result = pipeline.process_scene_and_query(
            query_text="What is the color of the aircraft fuselage?",
            task_name="Object Attribute",
            detected_boxes=[(1000, 1000, 1500, 1500), (6000, 6000, 6500, 6500)],
        )

        assert result["route_decision"] == "b3_selected"
        assert result["short_circuit"] is False
        # 1 global call + 2 active crops = 3 total forward passes
        assert result["n_vlm_forward_passes"] == 3
        assert len(result["selected_quadrants"]) == 2

    def test_disabled_shortcircuit_config(self):
        """When enable_router_shortcircuit is False, relational tasks do not short-circuit."""
        cfg = GroundedPyramidPipelineConfig(
            hidden_dim=256,
            num_heads=4,
            rope_dim=64,
            enable_router_shortcircuit=False,
        )
        pipeline = GroundedDualScalePyramid(cfg)
        result = pipeline.process_scene_and_query(
            query_text="Count the airplanes",
            task_name="Regional Counting",
            detected_boxes=[(500, 500, 800, 800)],
        )

        assert result["route_decision"] == "b1_direct"
        assert result["short_circuit"] is False
        assert result["n_vlm_forward_passes"] > 1

    def test_forward_multiscale_tokens_with_compression(self, pipeline):
        """With 2x2 compression enabled, 256-token streams compress to 64 tokens, fusing to 192 total tokens."""
        B, N_glob, D = 1, 256, 256  # 16x16 grid
        glob_tokens = torch.randn(B, N_glob, D)
        crop_tokens = [torch.randn(B, N_glob, D) for _ in range(2)]
        crop_bounds = [(0.0, 0.0, 0.5, 0.5), (0.5, 0.5, 1.0, 1.0)]

        fused = pipeline.forward_multiscale_tokens(
            global_overview_tokens=glob_tokens,
            crop_tokens_list=crop_tokens,
            crop_bounds_list=crop_bounds,
        )

        # 64 compressed global + 64 compressed crop1 + 64 compressed crop2 = 192 total tokens
        assert fused.shape == (B, 192, D)

    def test_forward_multiscale_tokens_without_compression(self):
        """With compression disabled, uncompressed 256-token streams fuse to 768 total tokens."""
        cfg = GroundedPyramidPipelineConfig(
            hidden_dim=128,
            num_heads=4,
            rope_dim=32,
            enable_compression=False,
        )
        pipeline = GroundedDualScalePyramid(cfg)
        B, N_glob, D = 1, 256, 128
        glob_tokens = torch.randn(B, N_glob, D)
        crop_tokens = [torch.randn(B, N_glob, D) for _ in range(2)]
        crop_bounds = [(0.0, 0.0, 0.5, 0.5), (0.5, 0.5, 1.0, 1.0)]

        fused = pipeline.forward_multiscale_tokens(
            global_overview_tokens=glob_tokens,
            crop_tokens_list=crop_tokens,
            crop_bounds_list=crop_bounds,
        )

        # 256 global + 256 crop1 + 256 crop2 = 768 total tokens
        assert fused.shape == (B, 768, D)
