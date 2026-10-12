"""Unit tests for Component 2: 15% Overlapped Hierarchical Quad-Tree."""
import pytest
from active_search.quad_tree import HierarchicalQuadTree, QuadrantNode


class TestHierarchicalQuadTree:
    """Tests for HierarchicalQuadTree partitioner and seam protection."""

    @pytest.fixture
    def tree(self):
        """Standard 8500x8500 quad-tree partitioner with 15% boundary overlap."""
        return HierarchicalQuadTree(
            image_width=8500,
            image_height=8500,
            max_depth=2,
            overlap_ratio=0.15,
        )

    def test_tree_construction_and_hierarchy(self, tree):
        """Quad-tree should build root, 4 level-1 nodes, and 16 level-2 nodes."""
        assert tree.root.level == 0
        assert tree.root.quadrant_name == "ROOT"
        assert tree.root.bounds == (0, 0, 8500, 8500)

        l1_nodes = tree.get_nodes_at_level(1)
        assert len(l1_nodes) == 4
        names_l1 = {n.quadrant_name for n in l1_nodes}
        assert names_l1 == {"NW", "NE", "SW", "SE"}

        l2_nodes = tree.get_nodes_at_level(2)
        assert len(l2_nodes) == 16

    def test_overlap_padding_dimensions(self, tree):
        """Level-1 quadrants should have padded dimensions expanded by 15%."""
        l1_nodes = tree.get_nodes_at_level(1)
        for node in l1_nodes:
            # Canonical quadrant is 4250 x 4250
            assert node.width == 4250
            assert node.height == 4250
            # Padded dimensions must be strictly larger than canonical dimensions
            assert node.padded_width > node.width
            assert node.padded_height > node.height
            # Bounds must be clamped within image boundaries [0, 8500]
            px0, py0, px1, py1 = node.padded_bounds
            assert px0 >= 0
            assert py0 >= 0
            assert px1 <= 8500
            assert py1 <= 8500

    def test_boundary_seam_protection_saved_by_padding(self, tree):
        """Objects lying right on quadrant boundaries should be severed without padding but saved with 15% overlap."""
        # Seam at x = 4250 (between NW and NE). Object spans x in [4200, 4300], y in [1000, 1100]
        seam_box = (4200, 1000, 4300, 1100)
        result = tree.check_object_severance(seam_box, use_padded=True)

        # Unpadded cuts straight through this box:
        assert result["severed_unpadded"] is True
        # 15% padding expands NW eastwards and NE westwards:
        assert result["severed_padded"] is False
        assert result["saved_by_padding"] is True

    def test_object_severance_horizontal_seam(self, tree):
        """Object spanning the horizontal equator seam y = 4250 should be saved by padding."""
        seam_box = (1000, 4200, 1100, 4300)
        result = tree.check_object_severance(seam_box, use_padded=True)

        assert result["severed_unpadded"] is True
        assert result["severed_padded"] is False
        assert result["saved_by_padding"] is True

    def test_object_center_quadrant_no_severance(self, tree):
        """Object well inside the North-West quadrant is not severed even without padding."""
        interior_box = (500, 500, 800, 800)
        result = tree.check_object_severance(interior_box, use_padded=True)

        assert result["severed_unpadded"] is False
        assert result["severed_padded"] is False
        assert result["saved_by_padding"] is False

    def test_quadrant_scoring_and_selection(self, tree):
        """Selection should prioritize quadrants containing target boxes."""
        # Target in NW (x: 1000..1200, y: 1000..1200) and target in SE (x: 6000..6200, y: 6000..6200)
        target_boxes = [
            (1000, 1000, 1200, 1200),
            (6000, 6000, 6200, 6200),
        ]
        selected = tree.score_and_select_quadrants(target_boxes, max_crops=2)
        assert len(selected) == 2
        selected_names = {n.quadrant_name for n in selected}
        assert "NW" in selected_names
        assert "SE" in selected_names

    def test_empty_targets_returns_root(self, tree):
        """When no target boxes are detected, should return the whole scene root node."""
        selected = tree.score_and_select_quadrants([], max_crops=2)
        assert len(selected) == 1
        assert selected[0].quadrant_name == "ROOT"

    def test_budget_constraint_capping(self, tree):
        """max_crops budget constraint should strictly cap number of selected nodes."""
        target_boxes = [
            (500, 500, 600, 600),     # NW
            (5000, 500, 5100, 600),   # NE
            (500, 5000, 600, 5100),   # SW
            (5000, 5000, 5100, 5100), # SE
        ]
        selected = tree.score_and_select_quadrants(target_boxes, max_crops=2)
        assert len(selected) == 2
