"""Unit tests for Component 4: Continuous Global 2D Rotary Position Embeddings (2D-RoPE)."""
import pytest
import torch

from geometry.global_2d_rope import ContinuousGlobal2DRoPE


class TestContinuousGlobal2DRoPE:
    """Tests for ContinuousGlobal2DRoPE and rotary transformations."""

    @pytest.fixture
    def rope_layer(self):
        """Standard 2D-RoPE layer with 64 dimensions."""
        return ContinuousGlobal2DRoPE(dim=64, theta=10000.0)

    def test_dim_divisibility_assertion(self):
        """dim must be divisible by 4 for dual 2D (x, y) split."""
        with pytest.raises(AssertionError):
            ContinuousGlobal2DRoPE(dim=62)

    def test_forward_output_shapes(self, rope_layer):
        """Outputs (cos, sin) tensors of shape (H * W, dim)."""
        grid_h, grid_w = 16, 16
        crop_bounds = (0.0, 0.0, 0.5, 0.5)

        cos, sin = rope_layer(grid_h, grid_w, crop_bounds)

        assert cos.shape == (256, 64)
        assert sin.shape == (256, 64)
        assert cos.dtype == torch.float32
        assert sin.dtype == torch.float32

    def test_values_bounded(self, rope_layer):
        """cos and sin values must be within [-1.0, 1.0] and cos^2 + sin^2 == 1."""
        grid_h, grid_w = 8, 8
        crop_bounds = (0.2, 0.3, 0.7, 0.8)

        cos, sin = rope_layer(grid_h, grid_w, crop_bounds)

        assert torch.all(cos >= -1.0 - 1e-6) and torch.all(cos <= 1.0 + 1e-6)
        assert torch.all(sin >= -1.0 - 1e-6) and torch.all(sin <= 1.0 + 1e-6)
        # Check trigonometric identity: cos^2 + sin^2 = 1
        sq_sum = (cos ** 2) + (sin ** 2)
        assert torch.allclose(sq_sum, torch.ones_like(sq_sum), atol=1e-5)

    def test_coordinate_anchoring_sensitivity(self, rope_layer):
        """Different spatial crop positions in the 8.5K image must produce distinct rotary embeddings."""
        grid_h, grid_w = 16, 16
        crop_nw = (0.0, 0.0, 0.5, 0.5)
        crop_se = (0.5, 0.5, 1.0, 1.0)

        cos_nw, sin_nw = rope_layer(grid_h, grid_w, crop_nw)
        cos_se, sin_se = rope_layer(grid_h, grid_w, crop_se)

        # NW and SE crops must NOT have identical position embeddings
        assert not torch.allclose(cos_nw, cos_se)
        assert not torch.allclose(sin_nw, sin_se)

    def test_global_unit_canvas_bounds(self, rope_layer):
        """Full unit canvas [0, 0, 1, 1] forward pass executes cleanly."""
        cos, sin = rope_layer(16, 16, (0.0, 0.0, 1.0, 1.0))
        assert cos.shape == (256, 64)

    def test_apply_rope_2d_tensor_rotation(self, rope_layer):
        """apply_rope_2d rotates query/key tensor preserving shape and norm."""
        B, num_heads, seq_len, head_dim = 2, 8, 64, 64
        x = torch.randn(B, num_heads, seq_len, head_dim)

        cos, sin = rope_layer(8, 8, (0.1, 0.1, 0.6, 0.6))
        rotated = ContinuousGlobal2DRoPE.apply_rope_2d(x, cos, sin)

        assert rotated.shape == x.shape
        # Rotary embedding is a unitary transformation, preserving vector norm per head
        norm_orig = torch.norm(x, dim=-1)
        norm_rot = torch.norm(rotated, dim=-1)
        assert torch.allclose(norm_orig, norm_rot, atol=1e-4)

    def test_dtype_preservation(self, rope_layer):
        """cos/sin embeddings respect specified dtype."""
        cos, sin = rope_layer(4, 4, (0.0, 0.0, 0.5, 0.5), dtype=torch.float64)
        assert cos.dtype == torch.float64
        assert sin.dtype == torch.float64
