"""Set-of-Mark (SoM) visual prompting module.

Overlays visual alphanumeric markers and bounding borders directly onto image
pixels, eliminating textual coordinate hallucinations and context bloat.
"""
from __future__ import annotations

from typing import List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont

from .base_detector import BoundingBox, GroundingCandidate


class VisualMarkerSOM:
    """Set-of-Mark visual annotation engine for crop grounding."""

    # High-contrast color palette for visual markers
    PALETTE: List[Tuple[int, int, int]] = [
        (239, 68, 68),    # Red
        (59, 130, 246),   # Blue
        (34, 197, 94),    # Green
        (245, 158, 11),   # Amber
        (168, 85, 247),   # Purple
        (236, 72, 153),   # Pink
        (20, 184, 166),   # Teal
        (249, 115, 22),   # Orange
    ]

    def __init__(self, line_width: int = 3, font_size: int = 18) -> None:
        self.line_width = line_width
        self.font_size = font_size

    def annotate_image(
        self,
        image: Image.Image,
        candidates: List[GroundingCandidate],
        draw_labels: bool = True,
    ) -> Image.Image:
        """Draws visual bounding boxes and alphanumeric tag badges onto image.

        Args:
            image: PIL RGB image.
            candidates: List of GroundingCandidate objects with bounding boxes.
            draw_labels: Whether to include label text beside the marker ID.

        Returns:
            Image.Image: Annotated PIL Image copy with overlaid visual marks.
        """
        img_out = image.copy().convert("RGBA")
        overlay = Image.new("RGBA", img_out.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)
        w_img, h_img = img_out.size

        try:
            font = ImageFont.load_default()
        except Exception:
            font = None

        for idx, cand in enumerate(candidates):
            color = self.PALETTE[idx % len(self.PALETTE)]
            b = cand.box

            # Denormalize if coordinates are normalized [0, 1]
            if b.xmax <= 1.0 and b.ymax <= 1.0:
                x0 = int(b.xmin * w_img)
                y0 = int(b.ymin * h_img)
                x1 = int(b.xmax * w_img)
                y1 = int(b.ymax * h_img)
            else:
                x0, y0, x1, y1 = int(b.xmin), int(b.ymin), int(b.xmax), int(b.ymax)

            # Clamp coordinates
            x0 = max(0, min(w_img - 1, x0))
            y0 = max(0, min(h_img - 1, y0))
            x1 = max(0, min(w_img - 1, x1))
            y1 = max(0, min(h_img - 1, y1))

            if x1 <= x0 or y1 <= y0:
                continue

            # Draw semi-transparent bounding rectangle
            border_color = color + (240,)
            fill_color = color + (40,)
            draw.rectangle([x0, y0, x1, y1], outline=border_color, width=self.line_width, fill=fill_color)

            # Draw tag badge [1], [2], ...
            marker_num = cand.marker_id or (idx + 1)
            tag_text = f"[{marker_num}]"
            if draw_labels and cand.label:
                tag_text += f" {cand.label}"

            # Badge background pill
            bx0 = x0
            by0 = max(0, y0 - 22)
            bx1 = bx0 + len(tag_text) * 8 + 10
            by1 = by0 + 20

            draw.rectangle([bx0, by0, bx1, by1], fill=color + (230,))
            draw.text((bx0 + 5, by0 + 3), tag_text, fill=(255, 255, 255, 255), font=font)

        # Composite overlay
        return Image.alpha_composite(img_out, overlay).convert("RGB")

    @staticmethod
    def format_som_prompt(candidates: List[GroundingCandidate], base_question: str) -> str:
        """Formats clean Set-of-Mark prompt instructing the VLM to refer to visual tags.

        Instead of injecting hundreds of text coordinates, this references only
        the clean visual marker IDs.
        """
        if not candidates:
            return base_question

        tag_list = ", ".join(f"[{c.marker_id}] {c.label}" for c in candidates if c.marker_id)
        instruction = (
            f"The image includes highlighted visual markers: {tag_list}. "
            f"Refer to these marked visual regions to answer: {base_question}"
        )
        return instruction
