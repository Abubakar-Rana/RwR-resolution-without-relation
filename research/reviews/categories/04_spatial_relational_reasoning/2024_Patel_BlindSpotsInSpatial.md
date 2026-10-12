# Paper Review: Investigating Spatial Reasoning Blind Spots in Vision-Language Models

| Field | Details |
| :--- | :--- |
| **Authors** | Mitesh Patel, Arpit Sharma, David Doermann |
| **Institution(s)** | University at Buffalo |
| **Publication Date / Venue** | 2024 / CVPRW 2024 |
| **arXiv ID / Link** | [2404.15201](https://arxiv.org/abs/2404.15201) |
| **Code Repository** | [https://github.com/UB-Vision/SpatialBlindSpots](https://github.com/UB-Vision/SpatialBlindSpots) |
| **Category** | Spatial & Relational Reasoning in VLMs |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
Identifies that aspect ratio resizing, patch downsampling, and spatial attention pooling collectively erase distance and orientation cues in standard VLM pipelines.

---

## 2. Abstract
> "We dissect the pipeline of modern MLLMs to identify where spatial information is lost. We show that early image resizing distorts aspect ratios, patch tokenization removes sub-patch coordinates, and transformer pooling flattens relational distance vectors."

---

## 3. Key Findings
1. Resizing non-square aerial images into square 336x336 inputs distorts angles by up to 35 degrees.
2. Sub-patch coordinate information is completely unrecoverable after initial patch projection.
3. Deep attention heads exhibit uniform attention over spatial distance.

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
Spatial distortion starts at image preprocessing and is magnified throughout transformer layers.

### Future Scope & Unsolved Frontiers
Aspect-ratio-preserving tokenization.

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `3 / 5` — *Moderate Diagnostic Prior*

### Relevance Rationale
Explains why naive resizing destroys cardinal angle calculations in aerial imagery.

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **Error Attribution**: Traces spatial distortion to early aspect-ratio warping and patch projection.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **End-to-End Solution**: Diagnostic study.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: Component-by-component spatial error analysis.
- **How our inquiry differs**: We preserve aspect ratios and use native dynamic resolution (NaViT) in Qwen2.5-VL.

---

## 8. Technical Deep-Dive & Architecture Specification

```mermaid
flowchart LR
    A[Visual Input] --> B[Encoder: CLIP ViT-L/14]
    B --> C[Projector: MLP]
    C --> D[LLM Backbone: Vicuna-7B]
    D --> E[Predictions: 576 tokens]
```

- **Vision Encoder**: `CLIP ViT-L/14`
- **Cross-Modal Projector**: `MLP`
- **Language Backbone**: `Vicuna-7B`
- **Visual Token Budget**: `576 tokens`

---

## 9. Actionable Takeaways for Our Codebase & Experiments
- [ ] **Preprocessing Rule**: Never stretch non-square aerial images into square inputs; preserve native aspect ratios.
