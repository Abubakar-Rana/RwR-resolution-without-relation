# Paper Review: Shikra: Unleashing Multimodal LLM's Referential Dialogue Magic

| Field | Details |
| :--- | :--- |
| **Authors** | Keqin Chen, Zhao Zhang, Weili Zeng, Richong Zhang, Feng Zhu, Rui Zhao |
| **Institution(s)** | SenseTime Research, Beihang University |
| **Publication Date / Venue** | 2023 / arXiv preprint |
| **arXiv ID / Link** | [2306.15195](https://arxiv.org/abs/2306.15195) |
| **Code Repository** | [https://github.com/shikras/shikra](https://github.com/shikras/shikra) |
| **Category** | Object Grounding, Detection & Open-Vocabulary Localization |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
Introduces natural coordinate representations into multimodal LLMs without specialized detection heads or extra vocabulary tokens, formatting bounding boxes as plain text $[x_{min}, y_{min}, x_{max}, y_{max}]$.

---

## 2. Abstract
> "We present Shikra, a multimodal LLM capable of referential dialogue. Shikra treats spatial coordinates as plain text numerical strings, handling Grounded VQA, Referring Expression Comprehension, and Referring Expression Generation within a unified autoregressive architecture."

---

## 3. Key Findings
1. Formatting coordinates as plain text strings $[x_{min}, y_{min}, x_{max}, y_{max}]$ works well on prominent, large objects.
2. However, precision degrades severely on objects smaller than 2% of image area.
3. Autoregressive coordinate generation incurs high latency for multi-object scenes.

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
Plain text coordinates are viable for coarse objects, but suffer high latency and low precision on dense tiny targets.

### Future Scope & Unsolved Frontiers
Continuous coordinate tokens and sparse regional decoding.

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `4 / 5` — *High Coordinate Prior*

### Relevance Rationale
Explains why Qwen2.5-VL (which adopts Shikra's plain text coordinate format) failed as a zero-shot detector in our baseline.

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **Plain Text Coordinate Format**: Standardized $[x_{min}, y_{min}, x_{max}, y_{max}]$ string representation in VLMs.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **Small Object Precision**: Text coordinate tokens cannot reliably localize tiny sub-30-pixel objects.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: Pioneered plain text coordinate formatting in modern VLMs.
- **How our inquiry differs**: We explain why this plain text coordinate approach collapses on 8K remote sensing and replace it with external detectors.

---

## 8. Technical Deep-Dive & Architecture Specification

```mermaid
flowchart LR
    A[Visual Input] --> B[Encoder: CLIP ViT-L/14]
    B --> C[Projector: Linear]
    C --> D[LLM Backbone: Vicuna-7B]
    D --> E[Predictions: 576 tokens]
```

- **Vision Encoder**: `CLIP ViT-L/14`
- **Cross-Modal Projector**: `Linear`
- **Language Backbone**: `Vicuna-7B`
- **Visual Token Budget**: `576 tokens`

---

## 9. Actionable Takeaways for Our Codebase & Experiments
- [ ] **Failure Diagnosis**: Cite Shikra to explain why Qwen2.5-VL's text bounding box generation failed on small targets.
- [ ] **Architectural Pivot**: Do not attempt to fix grounding by prompting text coordinates; use visual Set-of-Mark.
