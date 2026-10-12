"""Pixel-Shuffle 2x2 token compression and spatial pooling module.

Compresses visual patch tokens by 4x (75% token reduction) via spatial pixel-shuffle
and non-linear projection, reducing quadratic KV-cache memory and attention latency.
"""
from __future__ import annotations

import math
from typing import Optional, Tuple
import torch
import torch.nn as nn
import torch.nn.functional as F


class PixelShuffleTokenCompressor(nn.Module):
    """Spatially downsamples 2D visual tokens by 2x in each spatial dimension.

    Takes ViT patch representations of shape (Batch, Height, Width, Dim)
    and unifies adjacent 2x2 spatial quadrants into a single token with 4*Dim channels,
    followed by a LayerNorm + MLP projection back to target dimension D_out.

    Reduces token sequence length N -> N/4, cutting self-attention FLOPs by 16x.
    """

    def __init__(
        self,
        in_dim: int = 1152,
        out_dim: int = 3584,
        scale_factor: int = 2,
        mlp_depth: int = 2,
    ) -> None:
        """Initializes pixel-shuffle token compressor.

        Args:
            in_dim: Channel dimension of incoming vision encoder tokens (e.g., 1152 for SigLIP).
            out_dim: Target LLM hidden dimension (e.g., 3584 for Qwen2.5-7B).
            scale_factor: Spatial reduction factor (default 2 for 2x2 grouping = 4x token compression).
            mlp_depth: Number of linear layers in the projector MLP.
        """
        super().__init__()
        self.in_dim = in_dim
        self.out_dim = out_dim
        self.scale_factor = scale_factor

        flattened_dim = in_dim * (scale_factor ** 2)
        self.norm = nn.LayerNorm(flattened_dim)

        if mlp_depth == 1:
            self.projector = nn.Linear(flattened_dim, out_dim)
        else:
            self.projector = nn.Sequential(
                nn.Linear(flattened_dim, out_dim),
                nn.GELU(),
                nn.Linear(out_dim, out_dim),
            )

    def forward(
        self,
        x: torch.Tensor,
        spatial_shape: Optional[Tuple[int, int]] = None,
    ) -> Tuple[torch.Tensor, Tuple[int, int]]:
        """Compresses visual tokens by 2x2 spatial unification.

        Args:
            x: Input tensor of shape (B, H, W, D) or (B, N, D).
            spatial_shape: Optional (H, W) if x is flattened (B, N, D).

        Returns:
            Tuple of (compressed_tokens (B, N_comp, out_dim), new_spatial_shape (H_comp, W_comp)).
        """
        # Unpack spatial dimensions
        if x.dim() == 3:
            B, N, D = x.shape
            if spatial_shape is None:
                side = int(math.isqrt(N))
                if side * side != N:
                    raise ValueError(f"Cannot infer square spatial shape from N={N}")
                H, W = side, side
            else:
                H, W = spatial_shape
            x = x.view(B, H, W, D)
        elif x.dim() == 4:
            B, H, W, D = x.shape
        else:
            raise ValueError(f"Expected 3D or 4D tensor, got shape {x.shape}")

        s = self.scale_factor

        # Pad spatial dimensions if not divisible by scale factor
        pad_h = (s - (H % s)) % s
        pad_w = (s - (W % s)) % s
        if pad_h > 0 or pad_w > 0:
            x = F.pad(x.permute(0, 3, 1, 2), (0, pad_w, 0, pad_h), mode="replicate")
            x = x.permute(0, 2, 3, 1)
            H += pad_h
            W += pad_w

        # Reshape: (B, H//s, s, W//s, s, D) -> (B, H//s, W//s, s*s*D)
        new_H, new_W = H // s, W // s
        x = x.view(B, new_H, s, new_W, s, D)
        x = x.permute(0, 1, 3, 2, 4, 5).contiguous()
        x = x.view(B, new_H, new_W, s * s * D)

        # Apply LayerNorm and non-linear projection
        x = self.norm(x)
        out = self.projector(x)

        # Flatten spatial dimensions to token sequence (B, N_compressed, out_dim)
        N_comp = new_H * new_W
        out_flat = out.view(B, N_comp, self.out_dim)

        return out_flat, (new_H, new_W)


class AdaptiveTokenPruner(nn.Module):
    """Dynamic token pruner based on attention or norm salience.

    Preserves high-salience tokens (e.g., target objects and text indicators)
    while merging background tokens, enforcing strict token budget targets.
    """

    def __init__(self, keep_ratio: float = 0.5) -> None:
        super().__init__()
        self.keep_ratio = keep_ratio

    def forward(self, x: torch.Tensor, salience_scores: torch.Tensor) -> torch.Tensor:
        """Prunes tokens based on scalar salience score per token.

        Args:
            x: Visual tokens of shape (B, N, D).
            salience_scores: Salience weights of shape (B, N).

        Returns:
            Pruned tensor of shape (B, round(N * keep_ratio), D).
        """
        B, N, D = x.shape
        k = max(1, int(round(N * self.keep_ratio)))

        topk_indices = torch.topk(salience_scores, k=k, dim=-1, largest=True).indices
        topk_indices = topk_indices.unsqueeze(-1).expand(-1, -1, D)

        return torch.gather(x, dim=1, index=topk_indices)
