# Paper Review: Spatial Affordance Grounding in Embodied Multimodal Models

| Field | Details |
| :--- | :--- |
| **Authors** | Haotian Zhang, Boyuan Chen, Fei Xia |
| **Institution(s)** | Google DeepMind |
| **Publication Date / Venue** | 2024 / ECCV 2024 |
| **arXiv ID / Link** | [2407.16789](https://arxiv.org/abs/2407.16789) |
| **Code Repository** | [https://spatial-affordance.github.io](https://spatial-affordance.github.io) |
| **Category** | Embodied AI, 3D Vision-Language & Robot Navigation |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
Grounds language instructions directly in 2D spatial affordance heatmaps (where to grasp, where to navigate), showing that spatial heatmaps provide intuitive interfaces for downstream execution.

---

## 2. Abstract
> "We explore spatial affordance grounding in multimodal models. Rather than generating text coordinates, our model generates spatial heatmaps directly over image pixels, indicating feasible action regions with spatial confidence."

---

## 3. Key Findings
1. Spatial heatmaps over pixels are easier for vision models to predict than text coordinate strings.
2. Continuous heatmaps capture uncertainty naturally.
3. Downstream controllers sample execution points from heatmap peaks.

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
Spatial heatmaps over visual pixels provide a vastly superior interface for spatial localization than autoregressive coordinate tokens.

### Future Scope & Unsolved Frontiers
Multi-task affordance learning.

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `3 / 5` — *Moderate Embodied Prior*

### Relevance Rationale
Directly supports our visual prompt thesis: communicate spatial locations via visual pixel marks/heatmaps rather than text strings.

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **Pixel Affordance Heatmaps**: Predicts spatial targets as continuous heatmaps over pixels.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **Gigapixel Resolution**: Standard resolution images.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: Heatmap-based spatial grounding.
- **How our inquiry differs**: We use visual mark overlays (Set-of-Mark) directly on the input image canvas.

---

## 8. Technical Deep-Dive & Architecture Specification

```mermaid
flowchart LR
    A[Visual Input] --> B[Encoder: ViT-L with Heatmap Decoder]
    B --> C[Projector: Deconvolutional Upsampler]
    C --> D[LLM Backbone: PaLM-2]
    D --> E[Predictions: Native]
```

- **Vision Encoder**: `ViT-L with Heatmap Decoder`
- **Cross-Modal Projector**: `Deconvolutional Upsampler`
- **Language Backbone**: `PaLM-2`
- **Visual Token Budget**: `Native`

---

## 9. Actionable Takeaways for Our Codebase & Experiments
- [ ] **Interface Principle**: Pixel-space representations beat text-coordinate representations for spatial communication.
