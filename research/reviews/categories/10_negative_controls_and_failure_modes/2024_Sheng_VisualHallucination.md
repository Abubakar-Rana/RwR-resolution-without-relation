# Paper Review: Evaluating and Mitigating Visual Hallucinations in Large Multimodal Models

| Field | Details |
| :--- | :--- |
| **Authors** | Hao Sheng, Siyuan Huang, Tianhe Ren |
| **Institution(s)** | Tsinghua University |
| **Publication Date / Venue** | 2024 / CVPR 2024 |
| **arXiv ID / Link** | [2404.14892](https://arxiv.org/abs/2404.14892) |
| **Code Repository** | [https://github.com/THU-Sheng/VisualHallucination](https://github.com/THU-Sheng/VisualHallucination) |
| **Category** | Negative Controls, Optical Illusions & Representation Blindspots |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
Audits visual hallucination in multimodal models, showing that models hallucinate objects that frequently co-occur in text training data even when completely absent from the image.

---

## 2. Abstract
> "We evaluate object hallucination in MLLMs using the POPE benchmark and introduce a contrastive decoding mitigation. We find that language model priors override visual tokens, causing models to hallucinate co-occurring objects (e.g. hallucinating 'cars' in a parking lot that is empty)."

---

## 3. Key Findings
1. Language priors override visual tokens whenever visual resolution is ambiguous.
2. Hallucination rate reaches 45% on small objects under low resolution.
3. Contrastive decoding against a blinded vision baseline reduces hallucination.

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
Visual ambiguity directly triggers language model hallucination; grounding in high-resolution visual evidence is mandatory.

### Future Scope & Unsolved Frontiers
Grounded decoding verification.

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `4 / 5` — *Hallucination Diagnostic Prior*

### Relevance Rationale
Explains why downscaling aerial images causes hallucination of small objects.

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **Hallucination Attribution**: Proves visual ambiguity triggers linguistic hallucination.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **Gigapixel Remote Sensing**: Evaluated on COCO and POPE natural benchmarks.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: Hallucination diagnosis in VLMs.
- **How our inquiry differs**: We mitigate hallucination via real-time YOLO-World grounding rather than text-only contrastive decoding.

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
- [ ] **Grounding Benefit**: Grounding in explicit detector bounding boxes eliminates linguistic object hallucination.
