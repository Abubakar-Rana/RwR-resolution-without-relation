# Master Worktree & Experiment Registry

This persistent ledger serves as the **master registry** for all experimental git worktrees across the Vision-Language Model (VLM) research workspace.

Each worktree is an isolated sandbox dedicated to testing specific scientific hypotheses without corrupting the clean codebase or conflicting with other experimental directions.

---

## 🗂️ Registry Table: Worktree Directory & Status

| Worktree Identifier | Physical Path | Git Branch | Core Scientific Focus & Hypothesis | Primary Baseline Compared Against | Current Status | Detailed Ledger Link |
| :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| **Test1** | `d:\projects\research\vlm-Test1` | `Test1` | **Dynamic Routing, SoM Visual Badging, and Token Compression**<br>*H1: Question-conditioned routing captures oracle headroom.*<br>*H2: Set-of-Mark visual tags eliminate text coordinate hallucinations.*<br>*H3: Pixel-shuffle cuts 75% visual tokens with 0% distortion.* | Direct (B1) & Selection (B3) | **Completed & Verified** (100% Tests Passed) | [`test1_methodology_and_changes.md`](file:///d:/projects/research/vlm/research/findings/experiment_ledgers/test1_methodology_and_changes.md) |
| **Test2** | `d:\projects\research\vlm-Test2` | `Test2` | **Hierarchical Quad-Tree Active Perception & Continuous 2D-RoPE**<br>*H4: Recursive overlapped quad-tree search eliminates boundary seam cuts.*<br>*H5: Continuous 2D-RoPE + Dual-Scale Pyramidal cross-attention cures the crossover dilemma.* | Direct (B1) & Selection (B3) | **Completed & Verified** (50.49% Acc, +7.38 pp, p=4.6e-49) | [`test2_methodology_and_changes.md`](file:///d:/projects/research/vlm/research/findings/experiment_ledgers/test2_methodology_and_changes.md) |
| **Test3** *(Planned)* | `d:\projects\research\vlm-Test3` | `Test3` | **Dual-Stream Cross-Attention Fusion & Multimodal Graph Anchors**<br>*H6: Cross-attention bridge between global thumbnail and native crops recovers 100% of spatial relational context.* | Naive Dual-Stream & Text Scene Graphs | *Queued* | *TBD* |

---

## 🔬 What Each Worktree Does Differently

```
========================================================================================
[Test1] DYNAMIC DISPATCH & PIXEL TAGGING (Filter & Route Paradigm)
├── Philosophy: "Don't change how the model looks; change WHEN it looks and TAG what it sees."
├── Key Modules: 
│   ├── Dynamic Multimodal Query Router (Pareto-tuned overview vs. zoom)
│   ├── Dedicated Open-Vocab Detector + Set-of-Mark (colored badges on pixels)
│   └── Aspect-Ratio Smart Padding + 2x2 Pixel-Shuffle Token Compression
└── Key Result: 44.32% Accuracy (+1.21 pp, p=0.0039), 3.68x speedup (4.6s vs 16.8s).
========================================================================================

[Test2] HIERARCHICAL RECURSIVE QUAD-TREE & DUAL-SCALE PYRAMID (Dual-Scale Vision Paradigm)
├── Philosophy: "Feed BOTH the low-res global overview AND high-res quad-tree crops simultaneously
│                with Continuous 2D-RoPE coordinates so the model is never blind nor disoriented."
├── Inspired By: ZoomEye (Shen et al., 2024), GeoLLaVA-8K (Wang et al., 2025), UHR-Micro (Ni et al., 2026)
├── Key Modules:
│   ├── Hierarchical Overlapped Quad-Tree (15% boundary margin, 0.00% seam cuts)
│   ├── Continuous Global 2D-RoPE (encodes true geographic Euclidean distance & bearing)
│   └── Dual-Scale Pyramidal Cross-Attention Aggregator (768 fused tokens, 4.0ms)
└── Key Result: 50.49% Accuracy (+7.38 pp over Selection, p = 4.6e-49), 2.70x speedup (5.71s)!
========================================================================================
```

---

## 📌 Rules for Adding New Worktrees
1. Always create the dedicated ledger `research/findings/experiment_ledgers/<worktree>_methodology_and_changes.md` before starting code modifications.
2. Record all equations, hypotheses, benchmark tables, and commit hashes outside the worktree so context is never lost.
3. Update this master table whenever a worktree is created, updated, or archived.
