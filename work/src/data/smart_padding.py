"""Aspect-ratio preserving smart padding for ultra-high-resolution remote sensing crops.

Prevents geometric distortion of runways, roads, and buildings caused by
forced square image resizing while preserving reversible coordinate mapping.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np
from PIL import Image


@dataclass
class PaddingMetadata:
    """Stores transformation parameters for reversible coordinate mapping."""
    original_size: Tuple[int, int]     # (width, height)
    target_size: Tuple[int, int]       # (target_w, target_h)
    resized_size: Tuple[int, int]      # (new_w, new_h)
    scale_factor: float
    pad_left: int
    pad_top: int
    pad_right: int
    pad_bottom: int


class SmartPaddingTransform:
    """Isotropic resizer with constant color canvas padding."""

    def __init__(
        self,
        target_size: Union[int, Tuple[int, int]] = 1024,
        pad_color: Tuple[int, int, int] = (128, 128, 128),
        placement: str = "center",
        resample_filter: int = Image.Resampling.BICUBIC,
    ) -> None:
        """Initializes smart padding transform.

        Args:
            target_size: Target dimension as integer (square) or (width, height) tuple.
            pad_color: RGB fill color for canvas padding borders. Default neutral gray (128, 128, 128).
            placement: 'center' (symmetric padding) or 'top_left'.
            resample_filter: PIL resample algorithm.
        """
        if isinstance(target_size, int):
            self.target_size = (target_size, target_size)
        else:
            self.target_size = target_size

        self.pad_color = pad_color
        self.placement = placement
        self.resample_filter = resample_filter

    def __call__(self, image: Image.Image) -> Tuple[Image.Image, PaddingMetadata]:
        """Applies isotropic scaling and padding to an image.

        Args:
            image: PIL RGB image.

        Returns:
            Tuple of (padded_image, metadata).
        """
        orig_w, orig_h = image.size
        target_w, target_h = self.target_size

        if orig_w == target_w and orig_h == target_h:
            meta = PaddingMetadata(
                original_size=(orig_w, orig_h),
                target_size=(target_w, target_h),
                resized_size=(orig_w, orig_h),
                scale_factor=1.0,
                pad_left=0, pad_top=0, pad_right=0, pad_bottom=0,
            )
            return image.copy(), meta

        # Compute isotropic scale factor
        scale = min(target_w / orig_w, target_h / orig_h)
        new_w = max(1, int(round(orig_w * scale)))
        new_h = max(1, int(round(orig_h * scale)))

        # High-quality resize
        resized = image.resize((new_w, new_h), resample=self.resample_filter)

        # Create padded canvas
        padded_canvas = Image.new("RGB", (target_w, target_h), color=self.pad_color)

        if self.placement == "center":
            pad_left = (target_w - new_w) // 2
            pad_top = (target_h - new_h) // 2
        else:
            pad_left = 0
            pad_top = 0

        pad_right = target_w - new_w - pad_left
        pad_bottom = target_h - new_h - pad_top

        # Paste resized image onto canvas
        padded_canvas.paste(resized, (pad_left, pad_top))

        meta = PaddingMetadata(
            original_size=(orig_w, orig_h),
            target_size=(target_w, target_h),
            resized_size=(new_w, new_h),
            scale_factor=scale,
            pad_left=pad_left,
            pad_top=pad_top,
            pad_right=pad_right,
            pad_bottom=pad_bottom,
        )
        return padded_canvas, meta

    @staticmethod
    def map_box_to_padded(
        box: Tuple[float, float, float, float],
        meta: PaddingMetadata,
        normalized_in: bool = True,
        normalized_out: bool = True,
    ) -> Tuple[float, float, float, float]:
        """Transforms a bounding box from original coordinates to padded coordinates."""
        orig_w, orig_h = meta.original_size
        target_w, target_h = meta.target_size

        xmin, ymin, xmax, ymax = box
        if normalized_in:
            xmin *= orig_w
            ymin *= orig_h
            xmax *= orig_w
            ymax *= orig_h

        # Apply scale and translation
        px_min = xmin * meta.scale_factor + meta.pad_left
        py_min = ymin * meta.scale_factor + meta.pad_top
        px_max = xmax * meta.scale_factor + meta.pad_left
        py_max = ymax * meta.scale_factor + meta.pad_top

        if normalized_out:
            return (
                px_min / target_w,
                py_min / target_h,
                px_max / target_w,
                py_max / target_h,
            )
        return (px_min, py_min, px_max, py_max)

    @staticmethod
    def map_box_from_padded(
        box: Tuple[float, float, float, float],
        meta: PaddingMetadata,
        normalized_in: bool = True,
        normalized_out: bool = True,
    ) -> Tuple[float, float, float, float]:
        """Inverse-transforms a bounding box from padded space back to original space."""
        orig_w, orig_h = meta.original_size
        target_w, target_h = meta.target_size

        px_min, py_min, px_max, py_max = box
        if normalized_in:
            px_min *= target_w
            py_min *= target_h
            px_max *= target_w
            py_max *= target_h

        # Remove padding offset and divide by scale
        xmin = (px_min - meta.pad_left) / meta.scale_factor
        ymin = (py_min - meta.pad_top) / meta.scale_factor
        xmax = (px_max - meta.pad_left) / meta.scale_factor
        ymax = (py_max - meta.pad_top) / meta.scale_factor

        # Clamp to original image bounds
        xmin = max(0.0, min(float(orig_w), xmin))
        ymin = max(0.0, min(float(orig_h), ymin))
        xmax = max(0.0, min(float(orig_w), xmax))
        ymax = max(0.0, min(float(orig_h), ymax))

        if normalized_out:
            return (xmin / orig_w, ymin / orig_h, xmax / orig_w, ymax / orig_h)
        return (xmin, ymin, xmax, ymax)
