"""Unit tests for Component 5: Pixel-Shuffle 2x2 Token Compression & Spatial Pooling."""
import pytest
import torch

from models.token_compression import AdaptiveTokenPruner, PixelShuffleTokenCompressor


class TestPixelShuffleTokenCompressor:
    """Tests for 4x spatial token compression via 2x2 pixel-shuffle folding."""

    def test_compression_4d_input(self):
        """Input (B, H, W, D) of shape (2, 16, 16, 1024) is compressed to (2, 64, 1024)."""
        compressor = PixelShuffleTokenCompressor(
            in_dim=1024,
            out_dim=1024,
            scale_factor=2,
            mlp_depth=2,
        )
        x = torch.randn(2, 16, 16, 1024)
        out, (new_h, new_w) = compressor(x)

        assert new_h == 8
        assert new_w == 8
        assert out.shape == (2, 64, 1024)

    def test_compression_3d_input_flattened(self):
        """Input (B, N, D) of shape (1, 256, 512) is compressed 4x to (1, 64, 1024)."""
        compressor = PixelShuffleTokenCompressor(
            in_dim=512,
            out_dim=1024,
            scale_factor=2,
        )
        x = torch.randn(1, 256, 512)
        out, (new_h, new_w) = compressor(x)

        assert out.shape == (1, 64, 1024)
        assert new_h == 8
        assert new_w == 8

    def test_compression_with_explicit_spatial_shape(self):
        """Rectangular input with explicit spatial_shape=(16, 32) is compressed to (8, 16)."""
        compressor = PixelShuffleTokenCompressor(
            in_dim=256,
            out_dim=512,
            scale_factor=2,
        )
        x = torch.randn(2, 512, 256)  # 16 * 32 = 512 tokens
        out, (new_h, new_w) = compressor(x, spatial_shape=(16, 32))

        assert new_h == 8
        assert new_w == 16
        assert out.shape == (2, 128, 512)

    def test_single_layer_mlp_depth(self):
        """Supports mlp_depth=1 linear projector."""
        compressor = PixelShuffleTokenCompressor(
            in_dim=128,
            out_dim=256,
            scale_factor=2,
            mlp_depth=1,
        )
        x = torch.randn(1, 4, 4, 128)
        out, (new_h, new_w) = compressor(x)
        assert out.shape == (1, 4, 256)

    def test_odd_spatial_dimensions_padding(self):
        """Non-even spatial dimensions (e.g. 15x15) should be padded to 16x16 and compressed to 8x8."""
        compressor = PixelShuffleTokenCompressor(
            in_dim=64,
            out_dim=64,
            scale_factor=2,
        )
        x = torch.randn(1, 15, 15, 64)
        out, (new_h, new_w) = compressor(x)
        assert new_h == 8
        assert new_w == 8
        assert out.shape == (1, 64, 64)


class TestAdaptiveTokenPruner:
    """Tests for adaptive salience-based token pruning."""

    def test_token_pruning_ratio(self):
        """Prunes 50% of tokens based on salience weights."""
        pruner = AdaptiveTokenPruner(keep_ratio=0.5)
        B, N, D = 2, 100, 64
        x = torch.randn(B, N, D)
        salience = torch.rand(B, N)

        out = pruner(x, salience)
        assert out.shape == (2, 50, 64)

    def test_topk_selection_order(self):
        """Selected tokens must correspond to highest salience scores."""
        pruner = AdaptiveTokenPruner(keep_ratio=0.2)  # Keep top 2 out of 10
        B, N, D = 1, 10, 4
        x = torch.arange(10, dtype=torch.float32).view(1, 10, 1).expand(1, 10, 4)
        salience = torch.tensor([[0.1, 0.2, 0.9, 0.4, 0.0, 0.3, 0.8, 0.5, 0.2, 0.1]])

        out = pruner(x, salience)
        assert out.shape == (1, 2, 4)
        # Top-2 scores were at indices 2 (0.9) and 6 (0.8)
        kept_vals = set(out[0, :, 0].tolist())
        assert kept_vals == {2.0, 6.0}
