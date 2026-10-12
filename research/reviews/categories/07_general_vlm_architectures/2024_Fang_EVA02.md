# Paper Review: EVA-02: A New Turn for Vision Transformers

| Field | Details |
| :--- | :--- |
| **Authors** | Yuxin Fang, Quan Sun, Xinggang Wang, Tiejun Huang, Zhaoxiang Zhang, Yue Cao |
| **Institution(s)** | BAAI, HUST |
| **Publication Date / Venue** | 2024 / ICLR 2024 |
| **arXiv ID / Link** | [2303.11331](https://arxiv.org/abs/2303.11331) |
| **Code Repository** | [https://github.com/baaivision/EVA](https://github.com/baaivision/EVA) |
| **Category** | General Foundation VLMs & Multi-Crop Connectors |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
Introduces EVA-02, scaling masked image modeling with SwiGLU FFNs and sub-LN, achieving 90.0% top-1 on ImageNet and providing the visual backbone for CogVLM and EarthGPT.

---

## 2. Abstract
> "We present EVA-02, an advanced vision transformer architecture. By incorporating SwiGLU activations, sub-LayerNorm, and scaled masked image modeling pre-training, EVA-02 sets a new milestone in visual representation learning across classification, detection, and segmentation."

---

## 3. Key Findings
1. SwiGLU feedforward networks significantly improve representation capacity in vision transformers.
2. Masked image modeling preserves high-frequency edge details better than pure contrastive learning.
3. Excellent transfer to dense aerial detection.

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
Modern architectural enhancements (SwiGLU, sub-LN) stabilize large vision transformer pretraining and enhance edge localization.

### Future Scope & Unsolved Frontiers
Multimodal pretraining integration.

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `4 / 5` — *Foundational Vision Backbone*

### Relevance Rationale
High-performance visual backbone utilized in several remote sensing foundation models (EarthGPT).

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **EVA-02 Backbone**: High-capacity vision transformer with SwiGLU activations.
- **High-Frequency Detail**: Preserves sharp object edges.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **Multimodal LLM Decoder**: Vision backbone only.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: State-of-the-art vision transformer backbone.
- **How our inquiry differs**: We evaluate how EVA-02 features compare against SigLIP on remote sensing tile selection.

---

## 8. Technical Deep-Dive & Architecture Specification

```mermaid
flowchart LR
    A[Visual Input] --> B[Encoder: EVA-02-CLIP-E/14 (4.4B parameters)]
    B --> C[Projector: Linear / MLP]
    C --> D[LLM Backbone: None]
    D --> E[Predictions: Native]
```

- **Vision Encoder**: `EVA-02-CLIP-E/14 (4.4B parameters)`
- **Cross-Modal Projector**: `Linear / MLP`
- **Language Backbone**: `None`
- **Visual Token Budget**: `Native`

---

## 9. Actionable Takeaways for Our Codebase & Experiments
- [ ] **Encoder Option**: Test EVA-02 visual features for tile saliency scoring in ctsr/tiling/selection.py.
