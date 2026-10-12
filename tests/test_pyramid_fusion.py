"""Unit tests for Component 6: Dual-Scale Cross-Attention Pyramidal Aggregator."""
import pytest
import torch

from models.pyramid_fusion import DualScalePyramidAggregator, PyramidalFusionConfig, SpatialCrossAttention


class TestSpatialCrossAttention:
    """Tests for SpatialCrossAttention layer with continuous 2D-RoPE conditioning."""

    @pytest.fixture
    def config(self):
        return PyramidalFusionConfig(
            hidden_dim=256,
            num_heads=4,
            dropout=0.0,
            rope_dim=64,
        )

    def test_forward_without_rope(self, config):
        """Cross-attention executes cleanly without RoPE."""
        attn = SpatialCrossAttention(config)
        B, N_loc, N_glob, D = 2, 64, 64, 256
        loc_tokens = torch.randn(B, N_loc, D)
        glob_tokens = torch.randn(B, N_glob, D)

        out = attn(loc_tokens, glob_tokens)
        assert out.shape == (B, N_loc, D)

    def test_forward_with_rope(self, config):
        """Cross-attention conditions on (cos, sin) 2D rotary position embeddings."""
        attn = SpatialCrossAttention(config)
        B, N_loc, N_glob, D = 1, 16, 64, 256
        loc_tokens = torch.randn(B, N_loc, D)
        glob_tokens = torch.randn(B, N_glob, D)

        cos_loc = torch.ones(N_loc, 64)
        sin_loc = torch.zeros(N_loc, 64)
        cos_glob = torch.ones(N_glob, 64)
        sin_glob = torch.zeros(N_glob, 64)

        out = attn(
            loc_tokens,
            glob_tokens,
            cos_local=cos_loc,
            sin_local=sin_loc,
            cos_global=cos_glob,
            sin_global=sin_glob,
        )
        assert out.shape == (B, N_loc, D)


class TestDualScalePyramidAggregator:
    """Tests for DualScalePyramidAggregator multi-stream fusion."""

    @pytest.fixture
    def aggregator(self):
        config = PyramidalFusionConfig(
            hidden_dim=256,
            num_heads=4,
            gate_init=0.5,
            rope_dim=64,
        )
        return DualScalePyramidAggregator(config)

    def test_fuse_single_crop_with_overview(self, aggregator):
        """Fuses a single high-resolution crop with global overview tokens."""
        B, D = 2, 256
        # 8x8 = 64 tokens
        loc_tokens = torch.randn(B, 64, D)
        # 16x16 = 256 tokens
        glob_tokens = torch.randn(B, 256, D)
        crop_bounds = (0.0, 0.0, 0.5, 0.5)

        fused = aggregator.fuse_crop_with_overview(
            local_crop_tokens=loc_tokens,
            global_overview_tokens=glob_tokens,
            crop_norm_bounds=crop_bounds,
        )

        assert fused.shape == (B, 64, D)

    def test_aggregate_multiscale_sequence_with_global(self, aggregator):
        """Aggregates global overview + 2 crops into concatenated sequence."""
        B, D = 1, 256
        glob_tokens = torch.randn(B, 64, D)  # 64 global tokens
        crop1 = torch.randn(B, 64, D)
        crop2 = torch.randn(B, 64, D)
        bounds = [(0.0, 0.0, 0.5, 0.5), (0.5, 0.5, 1.0, 1.0)]

        out = aggregator.aggregate_multiscale_sequence(
            global_overview_tokens=glob_tokens,
            crop_tokens_list=[crop1, crop2],
            crop_bounds_list=bounds,
            include_global_tokens=True,
        )

        # 64 (global) + 64 (crop1) + 64 (crop2) = 192 total tokens
        assert out.shape == (B, 192, D)

    def test_aggregate_multiscale_sequence_without_global(self, aggregator):
        """When include_global_tokens=False, returns only crop tokens."""
        B, D = 1, 256
        glob_tokens = torch.randn(B, 64, D)
        crops = [torch.randn(B, 64, D) for _ in range(3)]
        bounds = [(0.0, 0.0, 0.5, 0.5)] * 3

        out = aggregator.aggregate_multiscale_sequence(
            global_overview_tokens=glob_tokens,
            crop_tokens_list=crops,
            crop_bounds_list=bounds,
            include_global_tokens=False,
        )

        # 3 * 64 = 192 tokens
        assert out.shape == (B, 192, D)

    def test_gradient_backpropagation(self, aggregator):
        """End-to-end gradients backpropagate through attention, MLP, and gating."""
        B, D = 1, 256
        loc_tokens = torch.randn(B, 16, D, requires_grad=True)
        glob_tokens = torch.randn(B, 16, D, requires_grad=True)
        crop_bounds = (0.1, 0.1, 0.5, 0.5)

        fused = aggregator.fuse_crop_with_overview(loc_tokens, glob_tokens, crop_bounds)
        loss = fused.sum()
        loss.backward()

        assert loc_tokens.grad is not None
        assert glob_tokens.grad is not None
        assert aggregator.gate.grad is not None
