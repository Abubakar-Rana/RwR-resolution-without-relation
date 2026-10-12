# Paper Review: Spurious Correlations in Vision-Language Pre-training: A Spatial Case Study

| Field | Details |
| :--- | :--- |
| **Authors** | Mitesh Patel, Arpit Sharma, David Doermann |
| **Institution(s)** | University at Buffalo |
| **Publication Date / Venue** | 2024 / CVPR 2024 |
| **arXiv ID / Link** | [2403.11290](https://arxiv.org/abs/2403.11290) |
| **Code Repository** | [https://github.com/UB-Vision/SpuriousSpatial](https://github.com/UB-Vision/SpuriousSpatial) |
| **Category** | Negative Controls, Optical Illusions & Representation Blindspots |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
Demonstrates that models learn spurious spatial correlations during pre-training (e.g. associating 'airplane' with 'above' or 'boat' with 'below'), causing systematic errors on aerial imagery where all objects are on a flat 2D ground plane.

---

## 2. Abstract
> "We investigate spurious spatial correlations in vision-language models. Models frequently rely on pre-trained semantic priors (e.g., sky is above, ground is below) to guess spatial answers, leading to systematic failure on nadir aerial imagery where all objects exist on an orthographic 2D plane."

---

## 3. Key Findings
1. Pretrained models possess strong vertical bias ('above'/'below') learned from gravity in web images.
2. Fails in nadir satellite imagery where 'above' is interpreted as 'North' but model treats it as vertical elevation.
3. Semantic categories carry spurious directional priors (e.g. 'planes are above clouds').

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
Terrestrial gravity biases in pre-trained models confound nadir 2D aerial spatial reasoning.

### Future Scope & Unsolved Frontiers
Gravity-invariant aerial pretraining.

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `3 / 5` — *Diagnostic Failure Analysis*

### Relevance Rationale
Explains why web-pretrained models confuse vertical elevation with 2D cardinal North.

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **Gravity Bias Diagnosis**: Traces aerial spatial errors to ground-level vertical gravity biases.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **Solution Architecture**: Diagnostic study.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: Spurious correlation analysis in VLMs.
- **How our inquiry differs**: We eliminate gravity confusion by explicitly prompting the model in cardinal coordinates (North/South/East/West).

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
- [ ] **Prompt Rule**: Avoid ambiguous terms like 'above' and 'below'; use strict cardinal terms 'North' and 'South'.
