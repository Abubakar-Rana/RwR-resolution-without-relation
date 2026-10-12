# 📄 Core Research Papers & Problem Statement

This directory houses the foundational manuscripts and drafts defining the research project and problem statement:

---

## 1. The Three Problem Statement Documents

| Document | File Name | Exact Title & Scope |
| :--- | :--- | :--- |
| **Initial Proposal** | [`CVC-27-Paper-NL.docx`](file:///d:/projects/research/vlm/work/paper/CVC-27-Paper-NL.docx) | **"Beyond Tiling: Hierarchical Visual-Language Reasoning for Ultra-High-Resolution Remote Sensing Imagery"**<br>Target: Computer Vision Conference 2027 (CVC 2027). Outlines the hierarchical pipeline vision on XLRS-Bench. |
| **Working Manuscript Draft** | [`CVC_2027_NL.pdf`](file:///d:/projects/research/vlm/work/paper/CVC_2027_NL.pdf) | **"Beyond Zoom: Cross-Tile Spatial-Relation Reasoning for Ultra-High-Resolution Remote-Sensing Vision-Language Models"**<br>Author: Hafiz Muhammad Abubakar (Planetary Health Informatics Lab, NDORMs, University of Oxford). Formalizes the cross-tile spatial-relation framework. |
| **Completed Empirical Paper** | [`main.pdf`](file:///d:/projects/research/vlm/work/paper/main.pdf) | **"Tile Selection Helps Perception but Hurts Spatial Reasoning in Ultra-High-Resolution Remote Sensing Visual Question Answering"**<br>Complete 13-page experimental paper reporting paired results on 3,080 XLRS-Bench items with Qwen2.5-VL-7B. Documents the +4.1 pp vs -4.5 pp crossover effect and the 66% null-object grounding failure. |

---

## 2. Core Problem Definition

- **The Goal**: Build an effective vision-language reasoning method for ultra-high-resolution (UHR) remote sensing images ($\sim 8,500 \times 8,500$ px) that preserves both **fine local details** (perception) and **global topological configuration** (spatial relations).
- **The Empirical Reality**:
  - Zooming into tiles raises perception accuracy by **+4.1 pp** ($42.6\% \to 46.7\%$) but collapses relational reasoning by **-4.5 pp** ($37.9\% \to 33.4\%$).
  - Supplying an explicit geometric relation graph in text produces a tightly bounded null result (**+0.0 pp**, 95% CI $[-2.1, +2.1]$) and acts as a distractor on perception.
  - Root cause: Zero-shot VLM object extraction fails on **66% of scenes**.
- **Next Research Objective**: Build the next evolution of this work — solving the grounding bottleneck, implementing adaptive global/local routing, and overcoming the crossover effect.
