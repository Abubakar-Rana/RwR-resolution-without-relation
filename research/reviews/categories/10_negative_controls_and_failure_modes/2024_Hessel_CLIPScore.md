# Paper Review: CLIPScore: Reference-Free Evaluation and Its Blind Spots

| Field | Details |
| :--- | :--- |
| **Authors** | Jack Hessel, Ari Holtzman, Maxwell Forbes, Ronan Le Bras, Yejin Choi |
| **Institution(s)** | Allen Institute for AI (AI2), University of Washington |
| **Publication Date / Venue** | 2021 / EMNLP 2021 |
| **arXiv ID / Link** | [2104.08718](https://arxiv.org/abs/2104.08718) |
| **Code Repository** | [https://github.com/jmhessel/clipscore](https://github.com/jmhessel/clipscore) |
| **Category** | Negative Controls, Optical Illusions & Representation Blindspots |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
Introduces CLIPScore for reference-free image captioning evaluation and rigorously documents its blind spots, showing that CLIPScore is blind to object counting errors and spatial relation inversions.

---

## 2. Abstract
> "We present CLIPScore, a reference-free metric for image caption evaluation. While CLIPScore correlates strongly with human judgment on semantic relevance, we identify critical blind spots: CLIPScore fails to penalize incorrect object counts or inverted spatial relationships."

---

## 3. Key Findings
1. CLIPScore cannot detect counting errors (hallucinating 5 cars instead of 2 yields high score).
2. Blind to spatial relation inversions ('above' vs 'below').
3. Warns against using CLIP-based metrics for spatial evaluation.

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
CLIP-based similarity scores must not be used as evaluators for spatial relations or object counts.

### Future Scope & Unsolved Frontiers
Compositional metrics.

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `3 / 5` — *Metric Blindspot Analysis*

### Relevance Rationale
Direct warning: do not use CLIP similarity to score spatial or counting outputs in our pipeline.

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **CLIP Blind Spot Analysis**: Documents counting and spatial relation blindness in CLIP similarity.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **VLM Generation Fix**: Metric analysis paper.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: Evaluation metric audit.
- **How our inquiry differs**: We heed this warning by avoiding CLIP-based scoring for relational tasks.

---

## 8. Technical Deep-Dive & Architecture Specification

```mermaid
flowchart LR
    A[Visual Input] --> B[Encoder: CLIP ViT-B/32]
    B --> C[Projector: Cosine similarity]
    C --> D[LLM Backbone: None]
    D --> E[Predictions: Global pooled vector]
```

- **Vision Encoder**: `CLIP ViT-B/32`
- **Cross-Modal Projector**: `Cosine similarity`
- **Language Backbone**: `None`
- **Visual Token Budget**: `Global pooled vector`

---

## 9. Actionable Takeaways for Our Codebase & Experiments
- [ ] **Metric Rule**: Never use CLIPScore to evaluate spatial VQA answers; use exact-match and symbolic verification.
