"""Hierarchical Quad-Tree Active Search Engine for Ultra-High-Resolution VLMs.

Implements recursive 4-quadrant spatial partitioning with boundary overlap padding
to prevent target severing on seams and dynamically focus VLM attention only where needed.
Inspired by ZoomEye (Shen et al., 2024) and ZoomEarth (Liu et al., 2025).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple
import numpy as np


@dataclass
class QuadrantNode:
    """Represents a node in the hierarchical spatial quad-tree."""

    node_id: str
    level: int  # 0 = Root (Global), 1 = 4 Quadrants, 2 = 16 Sub-quadrants
    quadrant_name: str  # 'ROOT', 'NW', 'NE', 'SW', 'SE'
    # Canonical bounds: [x_min, y_min, x_max, y_max] in pixels
    bounds: Tuple[int, int, int, int]
    # Padded bounds with boundary overlap to prevent seam severance
    padded_bounds: Tuple[int, int, int, int]
    # Normalized global coordinates: [u_min, v_min, u_max, v_max] in [0, 1]
    norm_bounds: Tuple[float, float, float, float]
    score: float = 0.0
    children: List[QuadrantNode] = field(default_factory=list)

    @property
    def width(self) -> int:
        return self.bounds[2] - self.bounds[0]

    @property
    def height(self) -> int:
        return self.bounds[3] - self.bounds[1]

    @property
    def padded_width(self) -> int:
        return self.padded_bounds[2] - self.padded_bounds[0]

    @property
    def padded_height(self) -> int:
        return self.padded_bounds[3] - self.padded_bounds[1]


class HierarchicalQuadTree:
    """Recursive spatial quad-tree decomposition engine with seam preservation."""

    def __init__(
        self,
        image_width: int,
        image_height: int,
        max_depth: int = 2,
        overlap_ratio: float = 0.15,
    ) -> None:
        """Initializes quad-tree partitioner.

        Args:
            image_width: Total image canvas width in pixels (e.g. 8500).
            image_height: Total image canvas height in pixels (e.g. 8500).
            max_depth: Maximum recursion level (0=root, 1=4 quadrants, 2=16 sub-quadrants).
            overlap_ratio: Overlap percentage added to quadrant boundaries (e.g. 0.15 = 15%).
        """
        self.img_w = image_width
        self.img_h = image_height
        self.max_depth = max_depth
        self.overlap_ratio = overlap_ratio
        self.root = self._build_tree(
            node_id="0",
            level=0,
            name="ROOT",
            x0=0,
            y0=0,
            x1=image_width,
            y1=image_height,
        )

    def _pad_bounds(
        self, x0: int, y0: int, x1: int, y1: int
    ) -> Tuple[int, int, int, int]:
        """Expands bounds by overlap_ratio clamped to image limits."""
        w = x1 - x0
        h = y1 - y0
        dx = int(w * self.overlap_ratio)
        dy = int(h * self.overlap_ratio)

        px0 = max(0, x0 - dx)
        py0 = max(0, y0 - dy)
        px1 = min(self.img_w, x1 + dx)
        py1 = min(self.img_h, y1 + dy)
        return (px0, py0, px1, py1)

    def _build_tree(
        self,
        node_id: str,
        level: int,
        name: str,
        x0: int,
        y0: int,
        x1: int,
        y1: int,
    ) -> QuadrantNode:
        """Recursively constructs quad-tree hierarchy."""
        padded = self._pad_bounds(x0, y0, x1, y1)
        norm = (
            x0 / self.img_w,
            y0 / self.img_h,
            x1 / self.img_w,
            y1 / self.img_h,
        )
        node = QuadrantNode(
            node_id=node_id,
            level=level,
            quadrant_name=name,
            bounds=(x0, y0, x1, y1),
            padded_bounds=padded,
            norm_bounds=norm,
        )

        if level < self.max_depth:
            mid_x = (x0 + x1) // 2
            mid_y = (y0 + y1) // 2

            # NW, NE, SW, SE
            quads = [
                (f"{node_id}_NW", "NW", x0, y0, mid_x, mid_y),
                (f"{node_id}_NE", "NE", mid_x, y0, x1, mid_y),
                (f"{node_id}_SW", "SW", x0, mid_y, mid_x, y1),
                (f"{node_id}_SE", "SE", mid_x, mid_y, x1, y1),
            ]
            for child_id, child_name, cx0, cy0, cx1, cy1 in quads:
                child = self._build_tree(
                    node_id=child_id,
                    level=level + 1,
                    name=child_name,
                    x0=cx0,
                    y0=cy0,
                    x1=cx1,
                    y1=cy1,
                )
                node.children.append(child)

        return node

    def get_nodes_at_level(self, level: int) -> List[QuadrantNode]:
        """Returns all quadrant nodes at a specific depth level."""
        results: List[QuadrantNode] = []

        def _traverse(node: QuadrantNode):
            if node.level == level:
                results.append(node)
            elif node.level < level:
                for child in node.children:
                    _traverse(child)

        _traverse(self.root)
        return results

    def check_object_severance(
        self,
        box: Tuple[int, int, int, int],
        use_padded: bool = True,
    ) -> Dict[str, bool]:
        """Checks if a bounding box is severed across boundaries.

        Args:
            box: Bounding box [x0, y0, x1, y1] in absolute image pixels.
            use_padded: If True, evaluates against padded boundaries.

        Returns:
            Dict containing whether the box is fully contained in at least one level-1 quadrant.
        """
        bx0, by0, bx1, by1 = box
        l1_nodes = self.get_nodes_at_level(1)

        fully_contained_unpadded = False
        fully_contained_padded = False

        for node in l1_nodes:
            # Check unpadded
            nx0, ny0, nx1, ny1 = node.bounds
            if bx0 >= nx0 and by0 >= ny0 and bx1 <= nx1 and by1 <= ny1:
                fully_contained_unpadded = True

            # Check padded
            px0, py0, px1, py1 = node.padded_bounds
            if bx0 >= px0 and by0 >= py0 and bx1 <= px1 and by1 <= py1:
                fully_contained_padded = True

        return {
            "severed_unpadded": not fully_contained_unpadded,
            "severed_padded": not fully_contained_padded,
            "saved_by_padding": (not fully_contained_unpadded) and fully_contained_padded,
        }

    def score_and_select_quadrants(
        self,
        target_boxes: Sequence[Tuple[int, int, int, int]],
        max_crops: int = 2,
    ) -> List[QuadrantNode]:
        """Selects the top-K quadrants covering the target boxes with minimum redundancy.

        Args:
            target_boxes: Sequence of detected candidate boxes.
            max_crops: Maximum number of high-res crops allowed (budget constraint).

        Returns:
            List of winning QuadrantNodes.
        """
        l1_nodes = self.get_nodes_at_level(1)
        if not target_boxes:
            # Return root node (whole scene overview)
            return [self.root]

        # Score nodes by target box coverage area
        for node in l1_nodes:
            px0, py0, px1, py1 = node.padded_bounds
            score = 0.0
            for bx0, by0, bx1, by1 in target_boxes:
                # Compute intersection
                ix0 = max(px0, bx0)
                iy0 = max(py0, by0)
                ix1 = min(px1, bx1)
                iy1 = min(py1, by1)
                if ix1 > ix0 and iy1 > iy0:
                    inter_area = (ix1 - ix0) * (iy1 - iy0)
                    box_area = (bx1 - bx0) * (by1 - by0)
                    score += inter_area / max(1.0, box_area)
            node.score = score

        # Sort descending
        sorted_nodes = sorted(l1_nodes, key=lambda n: n.score, reverse=True)
        # Select top nodes with non-zero score
        selected = [n for n in sorted_nodes if n.score > 0.0][:max_crops]
        if not selected:
            selected = [self.root]
        return selected
