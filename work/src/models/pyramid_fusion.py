"""Dual-Scale Pyramidal Token Fusion Engine for Ultra-High-Resolution VLMs.

Implements cross-scale cross-attention between a low-resolution global overview stream
and high-resolution quad-tree local crops with continuous 2D-RoPE geometric conditioning.
Allows the VLM to attend to microscopic fine-grained target details without losing
global geospatial topology and orientation.
Inspired by GeoLLaVA-8K (Wang et al., 2025), Mini-Gemini (Li et al., 2024), and UHR-Micro (Ni et al., 2026).
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import torch
import torch.nn as nn
import torch.nn.functional as F

from geometry.global_2d_rope import ContinuousGlobal2DRoPE


@dataclass
class PyramidalFusionConfig:
    """Configuration for Dual-Scale Pyramidal Token Aggregator."""

    hidden_dim: int = 1024  # Standard projector dimension
    num_heads: int = 8
    dropout: float = 0.05
    gate_init: float = 0.5  # Initial weight for global-to-local residual
    rope_dim: int = 128  # Dimensionality for 2D-RoPE (matches head_dim: 1024 // 8 = 128)


class SpatialCrossAttention(nn.Module):
    """Multi-head cross-attention layer with continuous 2D coordinate injection."""

    def __init__(self, config: PyramidalFusionConfig) -> None:
        super().__init__()
        self.hidden_dim = config.hidden_dim
        self.num_heads = config.num_heads
        self.head_dim = config.hidden_dim // config.num_heads
        assert (
            self.head_dim * config.num_heads == self.hidden_dim
        ), "hidden_dim must be divisible by num_heads."

        self.q_proj = nn.Linear(config.hidden_dim, config.hidden_dim, bias=False)
        self.k_proj = nn.Linear(config.hidden_dim, config.hidden_dim, bias=False)
        self.v_proj = nn.Linear(config.hidden_dim, config.hidden_dim, bias=False)
        self.out_proj = nn.Linear(config.hidden_dim, config.hidden_dim, bias=False)
        self.dropout = nn.Dropout(config.dropout)
        self.norm_q = nn.LayerNorm(config.hidden_dim)
        self.norm_kv = nn.LayerNorm(config.hidden_dim)

    def forward(
        self,
        local_tokens: torch.Tensor,
        global_tokens: torch.Tensor,
        cos_local: Optional[torch.Tensor] = None,
        sin_local: Optional[torch.Tensor] = None,
        cos_global: Optional[torch.Tensor] = None,
        sin_global: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """Executes cross-attention from local crop tokens (Q) to global overview tokens (K, V).

        Args:
            local_tokens: Tensor of shape (B, N_local, D).
            global_tokens: Tensor of shape (B, N_global, D).
            cos_local, sin_local: Optional 2D-RoPE embeddings for local tokens.
            cos_global, sin_global: Optional 2D-RoPE embeddings for global tokens.

        Returns:
            Context-enhanced local tokens of shape (B, N_local, D).
        """
        B, N_loc, D = local_tokens.shape
        _, N_glob, _ = global_tokens.shape

        q = self.norm_q(local_tokens)
        kv = self.norm_kv(global_tokens)

        # Projections: (B, num_heads, N, head_dim)
        q = self.q_proj(q).view(B, N_loc, self.num_heads, self.head_dim).transpose(1, 2)
        k = self.k_proj(kv).view(B, N_glob, self.num_heads, self.head_dim).transpose(1, 2)
        v = self.v_proj(kv).view(B, N_glob, self.num_heads, self.head_dim).transpose(1, 2)

        # Apply continuous 2D-RoPE if provided
        if cos_local is not None and sin_local is not None:
            q = ContinuousGlobal2DRoPE.apply_rope_2d(q, cos_local, sin_local)
        if cos_global is not None and sin_global is not None:
            k = ContinuousGlobal2DRoPE.apply_rope_2d(k, cos_global, sin_global)

        # Scaled dot-product attention
        scale = 1.0 / math.sqrt(self.head_dim)
        attn_weights = torch.matmul(q, k.transpose(-2, -1)) * scale
        attn_probs = F.softmax(attn_weights, dim=-1)
        attn_probs = self.dropout(attn_probs)

        # Output context: (B, num_heads, N_loc, head_dim) -> (B, N_loc, D)
        context = torch.matmul(attn_probs, v).transpose(1, 2).contiguous().view(B, N_loc, D)
        return self.out_proj(context)


class DualScalePyramidAggregator(nn.Module):
    """Integrates multi-scale visual streams into a unified multimodal token representation."""

    def __init__(self, config: Optional[PyramidalFusionConfig] = None) -> None:
        super().__init__()
        self.config = config or PyramidalFusionConfig()
        self.cross_attn = SpatialCrossAttention(self.config)
        self.rope = ContinuousGlobal2DRoPE(dim=self.config.rope_dim)

        # Learnable gating parameter to balance fine local details with macro layout
        self.gate = nn.Parameter(torch.tensor([self.config.gate_init], dtype=torch.float32))
        self.mlp = nn.Sequential(
            nn.Linear(self.config.hidden_dim, self.config.hidden_dim * 2),
            nn.GELU(),
            nn.Linear(self.config.hidden_dim * 2, self.config.hidden_dim),
            nn.Dropout(self.config.dropout),
        )
        self.norm = nn.LayerNorm(self.config.hidden_dim)

    def fuse_crop_with_overview(
        self,
        local_crop_tokens: torch.Tensor,
        global_overview_tokens: torch.Tensor,
        crop_norm_bounds: Tuple[float, float, float, float],
        grid_h: Optional[int] = None,
        grid_w: Optional[int] = None,
    ) -> torch.Tensor:
        """Fuses a single high-resolution quad-tree crop with global overview tokens.

        Args:
            local_crop_tokens: Tensor (B, N_local, D).
            global_overview_tokens: Tensor (B, N_global, D).
            crop_norm_bounds: [u_min, v_min, u_max, v_max] in [0, 1].
            grid_h: Token grid height. If None, inferred as isqrt(N_local).
            grid_w: Token grid width. If None, inferred as isqrt(N_local).

        Returns:
            Fused tokens of shape (B, N_local, D).
        """
        device = local_crop_tokens.device
        dtype = local_crop_tokens.dtype
        B, N_loc, D = local_crop_tokens.shape
        _, N_glob, _ = global_overview_tokens.shape

        if grid_h is None or grid_w is None:
            side_loc = int(math.isqrt(N_loc))
            grid_h, grid_w = side_loc, side_loc

        glob_side = int(math.isqrt(N_glob))

        # 1. Generate 2D-RoPE for local crop at its global coordinate window
        cos_loc, sin_loc = self.rope(
            local_grid_h=grid_h,
            local_grid_w=grid_w,
            crop_norm_bounds=crop_norm_bounds,
            device=device,
            dtype=dtype,
        )

        # 2. Generate 2D-RoPE for global overview spanning the full unit canvas [0, 0, 1, 1]
        cos_glob, sin_glob = self.rope(
            local_grid_h=glob_side,
            local_grid_w=glob_side,
            crop_norm_bounds=(0.0, 0.0, 1.0, 1.0),
            device=device,
            dtype=dtype,
        )

        # 3. Cross-attention: queries = local, keys = global
        context = self.cross_attn(
            local_tokens=local_crop_tokens,
            global_tokens=global_overview_tokens,
            cos_local=cos_loc,
            sin_local=sin_loc,
            cos_global=cos_glob,
            sin_global=sin_glob,
        )

        # 4. Gated residual connection
        fused = local_crop_tokens + (torch.sigmoid(self.gate) * context)
        fused = self.norm(fused + self.mlp(fused))
        return fused

    def aggregate_multiscale_sequence(
        self,
        global_overview_tokens: torch.Tensor,
        crop_tokens_list: List[torch.Tensor],
        crop_bounds_list: List[Tuple[float, float, float, float]],
        include_global_tokens: bool = True,
    ) -> torch.Tensor:
        """Aggregates all streams into a final sequence for the LLM backbone.

        Args:
            global_overview_tokens: Tensor (B, N_global, D).
            crop_tokens_list: List of high-res crop token tensors (each B, N_crop, D).
            crop_bounds_list: List of normalized bounding coordinates.
            include_global_tokens: If True, prepends the global overview tokens.

        Returns:
            Concatenated token sequence of shape (B, N_total, D).
        """
        fused_crops = []
        for crop_tokens, bounds in zip(crop_tokens_list, crop_bounds_list):
            fused_crop = self.fuse_crop_with_overview(
                local_crop_tokens=crop_tokens,
                global_overview_tokens=global_overview_tokens,
                crop_norm_bounds=bounds,
            )
            fused_crops.append(fused_crop)

        tokens_to_concat = []
        if include_global_tokens:
            tokens_to_concat.append(global_overview_tokens)
        tokens_to_concat.extend(fused_crops)

        return torch.cat(tokens_to_concat, dim=1)
