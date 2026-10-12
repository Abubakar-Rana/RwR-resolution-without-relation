# Paper Review: MoE-Vision: Dynamic Routing Across Modalities and Resolutions

| Field | Details |
| :--- | :--- |
| **Authors** | Yuan Li, Hao Zhang, Mengdi Li, Jiayan Teng |
| **Institution(s)** | Tsinghua University |
| **Publication Date / Venue** | 2024 / CVPR 2024 |
| **arXiv ID / Link** | [2404.18210](https://arxiv.org/abs/2404.18210) |
| **Code Repository** | [https://github.com/THU-Li/MoE-Vision](https://github.com/THU-Li/MoE-Vision) |
| **Category** | Dynamic Routing, Multi-Resolution & Cascaded VLM Systems |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
Routes visual tokens across multiple resolution branches dynamically inside the multimodal projector, allocating fine-resolution processing only to high-gradient image regions.

---

## 2. Abstract
> "We introduce MoE-Vision, dynamically routing visual tokens across multi-resolution encoder pathways. High-gradient and query-relevant tokens route through high-resolution experts, while low-frequency background routes through low-resolution experts."

---

## 3. Key Findings
1. Multi-resolution expert routing reduces visual token sequence length by 60%.
2. Preserves fine-grained perception on text and small objects.
3. Balances compute across heterogeneous image regions.

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
Routing visual tokens by spatial frequency and query relevance yields Pareto-optimal visual representations.

### Future Scope & Unsolved Frontiers
Generalizing to gigapixel aerial images.

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `4 / 5` — *High Architectural Prior*

### Relevance Rationale
Directly supports multi-resolution routing inside visual pipelines.

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **Multi-Resolution Expert Routing**: Routes tokens across different resolution encoders.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **Aerial Tiling Framework**: Evaluated on standard natural image benchmarks.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: Multi-resolution MoE projector.
- **How our inquiry differs**: We apply multi-resolution routing to gigapixel aerial scenes with task-conditioned gating.

---

## 8. Technical Deep-Dive & Architecture Specification

```mermaid
flowchart LR
    A[Visual Input] --> B[Encoder: Multi-Resolution ViT (Dual scale)]
    B --> C[Projector: MoE Projector (4 resolution experts)]
    C --> D[LLM Backbone: Vicuna-7B]
    D --> E[Predictions: Variable (60% reduction)]
```

- **Vision Encoder**: `Multi-Resolution ViT (Dual scale)`
- **Cross-Modal Projector**: `MoE Projector (4 resolution experts)`
- **Language Backbone**: `Vicuna-7B`
- **Visual Token Budget**: `Variable (60% reduction)`

---

## 9. Actionable Takeaways for Our Codebase & Experiments
- [ ] **Projector Routing**: Route crop tokens through lightweight downsamplers while retaining overview tokens intact.
