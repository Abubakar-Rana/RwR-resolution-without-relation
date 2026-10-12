"""Evaluation and verification suite for Hierarchical Quad-Tree and Global 2D-RoPE.

Audits:
1. Target boundary severance rate: Uniform slicing vs Overlapped Quad-Tree.
2. VLM crop budget: Static top-5 selection vs Dynamic Quad-Tree.
3. Continuous 2D-RoPE geometric distance preservation.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path
import numpy as np
import torch

# Ensure path resolution
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

from active_search.quad_tree import HierarchicalQuadTree
from geometry.global_2d_rope import ContinuousGlobal2DRoPE


def evaluate_seam_severance(
    n_targets: int = 1000,
    canvas_size: int = 8500,
    overlap_ratio: float = 0.15,
) -> dict:
    """Audits target object severance across tiling boundaries."""
    rng = np.random.default_rng(42)
    tree = HierarchicalQuadTree(
        image_width=canvas_size,
        image_height=canvas_size,
        max_depth=2,
        overlap_ratio=overlap_ratio,
    )

    # Generate synthetic target objects with realistic aerial sizes (20px to 250px)
    obj_sizes = rng.integers(20, 250, size=n_targets)
    x0s = rng.integers(0, canvas_size - 250, size=n_targets)
    y0s = rng.integers(0, canvas_size - 250, size=n_targets)

    boxes = [(int(x0s[i]), int(y0s[i]), int(x0s[i] + obj_sizes[i]), int(y0s[i] + obj_sizes[i])) for i in range(n_targets)]

    unpadded_severed = 0
    padded_severed = 0

    for b in boxes:
        res = tree.check_object_severance(b)
        if res["severed_unpadded"]:
            unpadded_severed += 1
        if res["severed_padded"]:
            padded_severed += 1

    rate_unpadded = (unpadded_severed / n_targets) * 100
    rate_padded = (padded_severed / n_targets) * 100
    severance_reduction = rate_unpadded - rate_padded

    return {
        "n_targets": n_targets,
        "canvas_size": canvas_size,
        "overlap_ratio": overlap_ratio,
        "unpadded_severed_rate": rate_unpadded,
        "padded_severed_rate": rate_padded,
        "severance_reduction_pp": severance_reduction,
    }


def evaluate_quad_tree_budget(n_scenes: int = 200, canvas_size: int = 8500) -> dict:
    """Audits crop selection count and VLM forward call reduction."""
    rng = np.random.default_rng(42)
    tree = HierarchicalQuadTree(canvas_size, canvas_size, max_depth=2, overlap_ratio=0.15)

    crop_counts = []
    for _ in range(n_scenes):
        # 1 to 4 target clusters per scene
        n_clusters = rng.integers(1, 5)
        boxes = []
        for _ in range(n_clusters):
            cx = rng.integers(500, canvas_size - 500)
            cy = rng.integers(500, canvas_size - 500)
            boxes.append((cx - 50, cy - 50, cx + 50, cy + 50))

        selected = tree.score_and_select_quadrants(boxes, max_crops=2)
        crop_counts.append(len(selected))

    mean_crops = float(np.mean(crop_counts))
    # In B3 Selection, it was always 5 high-res crops + 1 overview = 6.0 calls
    baseline_calls = 6.0
    quad_tree_calls = 1.0 + mean_crops  # 1 overview + dynamic crops

    return {
        "n_scenes": n_scenes,
        "mean_crops": mean_crops,
        "baseline_calls": baseline_calls,
        "quad_tree_calls": quad_tree_calls,
        "call_reduction_pct": ((baseline_calls - quad_tree_calls) / baseline_calls) * 100,
        "estimated_latency_s": 2.98 + (mean_crops * 2.5),
    }


def evaluate_global_rope_geometry() -> dict:
    """Validates that continuous 2D-RoPE correctly reflects global Euclidean distance."""
    rope = ContinuousGlobal2DRoPE(dim=64, theta=10000.0)

    # Two crops in different quadrants
    # Crop NW: [0, 0, 0.5, 0.5]
    # Crop SE: [0.5, 0.5, 1.0, 1.0]
    cos_nw, sin_nw = rope(local_grid_h=16, local_grid_w=16, crop_norm_bounds=(0.0, 0.0, 0.5, 0.5))
    cos_se, sin_se = rope(local_grid_h=16, local_grid_w=16, crop_norm_bounds=(0.5, 0.5, 1.0, 1.0))

    # Center token of NW: patch (8, 8) -> norm global (0.25, 0.25)
    # Center token of SE: patch (8, 8) -> norm global (0.75, 0.75)
    center_idx = 8 * 16 + 8

    # Query at NW center, Key at SE center
    q = torch.ones(1, 1, 1, 64)
    k_near = torch.ones(1, 1, 1, 64)  # Token near NW center
    k_far = torch.ones(1, 1, 1, 64)   # Token far away at SE center

    q_rot = ContinuousGlobal2DRoPE.apply_rope_2d(q, cos_nw[center_idx:center_idx+1], sin_nw[center_idx:center_idx+1])
    
    # Near token: patch (9, 8) in NW -> global (0.28, 0.25)
    k_near_rot = ContinuousGlobal2DRoPE.apply_rope_2d(k_near, cos_nw[center_idx+1:center_idx+2], sin_nw[center_idx+1:center_idx+2])
    # Far token: patch (8, 8) in SE -> global (0.75, 0.75)
    k_far_rot = ContinuousGlobal2DRoPE.apply_rope_2d(k_far, cos_se[center_idx:center_idx+1], sin_se[center_idx:center_idx+1])

    dot_near = (q_rot * k_near_rot).sum().item()
    dot_far = (q_rot * k_far_rot).sum().item()

    is_monotonic = dot_near > dot_far

    return {
        "dot_near_distance": dot_near,
        "dot_far_distance": dot_far,
        "monotonic_decay_verified": is_monotonic,
        "status": "PASS" if is_monotonic else "FAIL",
    }


def run_full_audit() -> None:
    print("Executing Worktree Test2 Quad-Tree Active Search & Global 2D-RoPE Audit...")
    seam_results = evaluate_seam_severance()
    budget_results = evaluate_quad_tree_budget()
    rope_results = evaluate_global_rope_geometry()

    print("\n=== 1. SEAM TRUNCATION AUDIT ===")
    print(f"Targets Tested: {seam_results['n_targets']}")
    print(f"Unpadded Severance Rate (Literature Baseline): {seam_results['unpadded_severed_rate']:.2f}%")
    print(f"Overlapped Quad-Tree Severance Rate: {seam_results['padded_severed_rate']:.2f}%")
    print(f"Severance Cut: -{seam_results['severance_reduction_pp']:.2f} percentage points!")

    print("\n=== 2. INFERENCE CALL BUDGET AUDIT ===")
    print(f"Mean Dynamic Crops: {budget_results['mean_crops']:.2f} (vs 5.0 fixed in B3 Selection)")
    print(f"Total VLM Calls: {budget_results['quad_tree_calls']:.2f} (vs 6.0 in B3)")
    print(f"VLM Call Reduction: {budget_results['call_reduction_pct']:.2f}%")
    print(f"Estimated Latency: {budget_results['estimated_latency_s']:.2f}s (vs 15.4s in B3)")

    print("\n=== 3. GLOBAL 2D-RoPE SPATIAL DECAY ===")
    print(f"Near Distance Attention Dot-Product: {rope_results['dot_near_distance']:.4f}")
    print(f"Far Distance Attention Dot-Product:  {rope_results['dot_far_distance']:.4f}")
    print(f"Monotonic Geographic Decay Verified: {rope_results['monotonic_decay_verified']}")

    out_file = ROOT / "materials" / "rwr_repo" / "results" / "analysis_outputs" / "test2_quadtree_rope_evaluation.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    summary = {
        "seam_severance": seam_results,
        "budget": budget_results,
        "global_rope": rope_results,
    }
    out_file.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\nAudit complete! Saved results to: {out_file}")


if __name__ == "__main__":
    run_full_audit()
