"""Continuous Global 2D Rotary Position Embeddings (Global 2D-RoPE).

Anchors high-resolution local crops directly into the continuous global coordinate frame
of ultra-high-resolution (8.5K x 8.5K) remote sensing scenes.
Eliminates coordinate de-synchronization and spatial disorientation during active zoom.
Inspired by UHR-Micro (Ni et al., IEEE TGRS 2026) and 2D-RoPE (Qwen2.5-VL / InternVL).
"""
from __future__ import annotations

import math
from typing import Dict, Optional, Tuple
import torch
import torch.nn as nn


class ContinuousGlobal2DRoPE(nn.Module):
    """Computes continuous 2D Rotary Position Embeddings anchored to global map coordinates."""

    def __init__(
        self,
        dim: int = 64,
        theta: float = 10000.0,
        max_scale: float = 1.0,
    ) -> None:
        """Initializes continuous 2D-RoPE layer.

        Args:
            dim: Dimension of positional features (must be even, typically head_dim // 2).
            theta: Base frequency for rotary embeddings.
            max_scale: Maximum coordinate scale (normalized to 1.0 for unit square [0, 1]^2).
        """
        super().__init__()
        assert dim % 4 == 0, f"Dimension {dim} must be divisible by 4 for dual 2D (x, y) split."
        self.dim = dim
        self.dim_half = dim // 2  # dim for x, dim for y
        self.theta = theta
        self.max_scale = max_scale

        # Geometric frequencies: theta^(-2i / d)
        inv_freq = 1.0 / (
            theta ** (torch.arange(0, self.dim_half, 2).float() / self.dim_half)
        )
        self.register_buffer("inv_freq", inv_freq, persistent=False)

    def forward(
        self,
        local_grid_h: int,
        local_grid_w: int,
        crop_norm_bounds: Tuple[float, float, float, float],
        device: Optional[torch.device] = None,
        dtype: Optional[torch.dtype] = None,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """Generates continuous (cos, sin) rotary embeddings for a high-resolution crop.

        Args:
            local_grid_h: Number of patch tokens along height in the crop (e.g. 32).
            local_grid_w: Number of patch tokens along width in the crop (e.g. 32).
            crop_norm_bounds: Global normalized bounding box of the crop [u_min, v_min, u_max, v_max] in [0, 1].
            device: Target torch device.
            dtype: Target torch data type.

        Returns:
            Tuple of (cos_emb, sin_emb) of shape (local_grid_h * local_grid_w, dim).
        """
        u0, v0, u1, v1 = crop_norm_bounds

        # Generate normalized coordinate meshes across the crop
        # u is horizontal (X), v is vertical (Y)
        u_coords = torch.linspace(u0, u1, local_grid_w, device=device, dtype=torch.float32)
        v_coords = torch.linspace(v0, v1, local_grid_h, device=device, dtype=torch.float32)

        # 2D Grid coordinates: shape (local_grid_h, local_grid_w)
        v_mesh, u_mesh = torch.meshgrid(v_coords, u_coords, indexing="ij")
        u_flat = u_mesh.reshape(-1)  # (N_tokens,)
        v_flat = v_mesh.reshape(-1)  # (N_tokens,)

        # Compute outer products with inverse frequencies
        # shape: (N_tokens, dim_quarter)
        inv_freq = self.inv_freq.to(device=device)
        freqs_u = torch.outer(u_flat, inv_freq)
        freqs_v = torch.outer(v_flat, inv_freq)

        # Replicate dual frequencies for rotary pairing: (cos, sin) per frequency
        freqs_u = torch.repeat_interleave(freqs_u, 2, dim=-1)  # (N_tokens, dim_half)
        freqs_v = torch.repeat_interleave(freqs_v, 2, dim=-1)  # (N_tokens, dim_half)

        # Concatenate X and Y frequencies into full head dimension
        # (N_tokens, dim)
        freqs_2d = torch.cat([freqs_u, freqs_v], dim=-1)

        cos_emb = torch.cos(freqs_2d).to(dtype=dtype)
        sin_emb = torch.sin(freqs_2d).to(dtype=dtype)

        return cos_emb, sin_emb

    @staticmethod
    def apply_rope_2d(
        x: torch.Tensor,
        cos: torch.Tensor,
        sin: torch.Tensor,
    ) -> torch.Tensor:
        """Applies 2D rotary position embeddings to query or key tensor.

        Args:
            x: Tensor of shape (batch, num_heads, seq_len, head_dim).
            cos: Tensor of shape (seq_len, head_dim).
            sin: Tensor of shape (seq_len, head_dim).

        Returns:
            Rotated tensor of identical shape.
        """
        # Rotate half: [-x2, x1, -x4, x3, ...]
        x_reshaped = x.reshape(*x.shape[:-1], -1, 2)
        x1 = x_reshaped[..., 0]
        x2 = x_reshaped[..., 1]
        x_rot = torch.stack([-x2, x1], dim=-1).flatten(start_dim=-2)

        return (x * cos) + (x_rot * sin)
