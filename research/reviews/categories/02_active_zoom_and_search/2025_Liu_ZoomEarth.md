# Paper Review: ZoomEarth: Active Perception for Ultra-High-Resolution Geospatial Vision-Language Tasks

| Field | Details |
| :--- | :--- |
| **Authors** | Rui Liu, Fangrun Wang, Haoliang Wang, Wen Yang |
| **Institution(s)** | Wuhan University |
| **Publication Date / Venue** | 2025 / arXiv preprint |
| **arXiv ID / Link** | [2502.19011](https://arxiv.org/abs/2502.19011) |
| **Code Repository** | [https://github.com/WHU-USI/ZoomEarth](https://github.com/WHU-USI/ZoomEarth) |
| **Category** | Active Zoom, Guided Visual Search & Dynamic Tiling |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
ZoomEarth implements an active perception agent that interacts with gigapixel remote sensing images through dynamic zooming, panning, and crop inspection using reinforcement learning.

---

## 2. Abstract
> "Fixed tiling strategies waste compute on uninformative background patches and shatter scene topology. ZoomEarth treats gigapixel image comprehension as an active perception task, training a policy model to iteratively zoom, pan, and focus on relevant regions guided by the query."

---

## 3. Key Findings
1. Active zooming cuts token budget by 65% compared to uniform tiling.
2. Achieves high accuracy on fine object recognition but incurs multi-step inference latency.
3. Search policy occasionally gets trapped in local visual distractors.

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
Question-conditioned active search outperforms uniform grid slicing in token efficiency.

### Future Scope & Unsolved Frontiers
Single-step multi-scale routing and reducing sequential search latency.

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `5 / 5` — *Critical Direct Baseline*

### Relevance Rationale
Direct competitor and baseline: explores active zoom on gigapixel imagery.

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **Active Perception Policy**: Reinforcement learning policy for crop selection.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **Low Latency**: Multi-step sequential zoom requires 5-8 LLM generation steps per query.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: Directly tackles zoom in remote sensing, but multi-turn latency is high.
- **How our inquiry differs**: We use single-turn dynamic routing and open-vocabulary detection, avoiding multi-turn latency.

---

## 8. Technical Deep-Dive & Architecture Specification

```mermaid
flowchart LR
    A[Visual Input] --> B[Encoder: CLIP ViT-L/14 with Dynamic Affine Crop]
    B --> C[Projector: MLP]
    C --> D[LLM Backbone: Qwen2-VL-7B]
    D --> E[Predictions: 1,200 tokens per step (up to 5 steps)]
```

- **Vision Encoder**: `CLIP ViT-L/14 with Dynamic Affine Crop`
- **Cross-Modal Projector**: `MLP`
- **Language Backbone**: `Qwen2-VL-7B`
- **Visual Token Budget**: `1,200 tokens per step (up to 5 steps)`

---

## 9. Actionable Takeaways for Our Codebase & Experiments
- [ ] **Direct Baseline**: Compare accuracy and latency against ZoomEarth.
