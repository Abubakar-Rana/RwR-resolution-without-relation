# Paper Review: Relative Coordinate Embeddings for Grounded Multimodal Transformers

| Field | Details |
| :--- | :--- |
| **Authors** | Zhenshi Li, Diliyaer Muhtar, Xueliang Lu |
| **Institution(s)** | Nanjing University |
| **Publication Date / Venue** | 2024 / CVPR 2024 |
| **arXiv ID / Link** | [2405.04112](https://arxiv.org/abs/2405.04112) |
| **Code Repository** | [https://github.com/NJU-LHRS/RelCoord](https://github.com/NJU-LHRS/RelCoord) |
| **Category** | Spatial & Relational Reasoning in VLMs |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
Replaces absolute coordinate tokens with relative offset vectors between detected objects, showing that relative coordinates are easier for language models to process than absolute grid coordinates.

---

## 2. Abstract
> "We demonstrate that predicting absolute bounding coordinates $[x_1, y_1, x_2, y_2]$ is inherently difficult for autoregressive LLMs due to scale sensitivity. We propose Relative Coordinate Embeddings (RelCoord), parameterizing object locations as relative displacement vectors from anchor landmarks."

---

## 3. Key Findings
1. Relative coordinates improve spatial reasoning by +11.8% over absolute coordinates.
2. Reduces coordinate token hallucination.
3. Aligns with human spatial description conventions ('50 meters north of the tower').

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
Relative displacement from landmark anchors is far more robust than absolute pixel coordinates.

### Future Scope & Unsolved Frontiers
Automated landmark selection in remote sensing.

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `4 / 5` — *High Architectural Prior*

### Relevance Rationale
Provides a robust mathematical representation for spatial relationships between aerial objects.

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **Relative Coordinate Parameterization**: Encodes positions as $(\Delta x, \Delta y, \Delta d)$ relative to visual anchors.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **Gigapixel Tiling Integration**: Tested on single-crop scenes.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: Relative coordinate representations in VLMs.
- **How our inquiry differs**: We apply relative landmark anchoring across the global overview image and local crops.

---

## 8. Technical Deep-Dive & Architecture Specification

```mermaid
flowchart LR
    A[Visual Input] --> B[Encoder: CLIP ViT-L/14]
    B --> C[Projector: Relative MLP]
    C --> D[LLM Backbone: Vicuna-7B]
    D --> E[Predictions: 576 tokens]
```

- **Vision Encoder**: `CLIP ViT-L/14`
- **Cross-Modal Projector**: `Relative MLP`
- **Language Backbone**: `Vicuna-7B`
- **Visual Token Budget**: `576 tokens`

---

## 9. Actionable Takeaways for Our Codebase & Experiments
- [ ] **Coordinate Format**: When prompting the model with coordinates, use relative vectors from scene center.
