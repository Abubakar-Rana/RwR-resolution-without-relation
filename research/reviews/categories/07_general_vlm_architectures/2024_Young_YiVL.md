# Paper Review: Yi-VL: Large Multimodal Models from 01.AI

| Field | Details |
| :--- | :--- |
| **Authors** | Alex Young, Bei Chen, Chao Li, Chengen Huang, Ge Zhang, Guanwei Ding |
| **Institution(s)** | 01.AI |
| **Publication Date / Venue** | 2024 / arXiv preprint |
| **arXiv ID / Link** | [2403.04780](https://arxiv.org/abs/2403.04780) |
| **Code Repository** | [https://github.com/01-ai/Yi](https://github.com/01-ai/Yi) |
| **Category** | General Foundation VLMs & Multi-Crop Connectors |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
Develops Yi-VL (6B and 34B), scaling multimodal language models using dual ViT encoders (CLIP ViT-H and OpenCLIP ViT-G) concatenated through a multi-layer MLP.

---

## 2. Abstract
> "We present Yi-VL, built on the Yi language model family. Yi-VL combines features from two distinct vision encoders to capture complementary semantic and low-level representations, achieving strong multimodal reasoning."

---

## 3. Key Findings
1. Concatenating two distinct vision encoders (CLIP + OpenCLIP) enriches visual representations.
2. Scales successfully to 34B language parameters.
3. Higher parameter size improves complex reasoning but does not fix small object blindness.

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
Dual vision encoders provide complementary features, but language parameter scaling alone cannot overcome input resolution limits.

### Future Scope & Unsolved Frontiers
Dynamic resolution tiling.

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `3 / 5` — *Moderate Architectural Prior*

### Relevance Rationale
Shows that simply scaling LLM parameters from 7B to 34B does not fix input resolution limitations.

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **Dual Vision Encoder Fusion**: Fuses features from two distinct ViT backbones.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **High-Resolution Tiling**: Fixed 448x448 resolution.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: Dual-encoder architecture.
- **How our inquiry differs**: We tackle the resolution bottleneck algorithmically rather than relying purely on LLM parameter scaling.

---

## 8. Technical Deep-Dive & Architecture Specification

```mermaid
flowchart LR
    A[Visual Input] --> B[Encoder: Dual ViT (ViT-H-14 + ViT-bigG)]
    B --> C[Projector: Three-layer MLP]
    C --> D[LLM Backbone: Yi-34B / Yi-6B]
    D --> E[Predictions: 1,024 tokens]
```

- **Vision Encoder**: `Dual ViT (ViT-H-14 + ViT-bigG)`
- **Cross-Modal Projector**: `Three-layer MLP`
- **Language Backbone**: `Yi-34B / Yi-6B`
- **Visual Token Budget**: `1,024 tokens`

---

## 9. Actionable Takeaways for Our Codebase & Experiments
- [ ] **Parameter Insight**: Model parameter scaling (7B -> 34B) does not solve the resolution dilemma; spatial routing is required.
