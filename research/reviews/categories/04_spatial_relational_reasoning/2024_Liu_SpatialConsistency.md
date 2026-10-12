# Paper Review: Spatial Consistency Probing in Large Multimodal Models

| Field | Details |
| :--- | :--- |
| **Authors** | Shuai Liu, Kexin Cheng, Xiang Bai |
| **Institution(s)** | Huazhong University of Science and Technology |
| **Publication Date / Venue** | 2024 / ECCV 2024 |
| **arXiv ID / Link** | [2407.16540](https://arxiv.org/abs/2407.16540) |
| **Code Repository** | [https://github.com/HUST-VL/SpatialConsistency](https://github.com/HUST-VL/SpatialConsistency) |
| **Category** | Spatial & Relational Reasoning in VLMs |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
Probes spatial consistency by asking logically paired questions (e.g., 'Is A north of B?' and 'Is B south of A?'), showing models contradict their own spatial answers 42% of the time.

---

## 2. Abstract
> "We evaluate spatial consistency in MLLMs using symmetric and transitive question pairs. Across 10 top models, we find that models contradict their own answers in 42% of spatial queries, revealing that spatial answers are generated from ungrounded token probability distributions rather than consistent mental models."

---

## 3. Key Findings
1. 42% internal contradiction rate on inverse spatial questions ('A is left of B' vs 'B is right of A').
2. Models lack a unified spatial coordinate model.
3. Contradictions occur even when visual perception of individual objects is correct.

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
Autoregressive generation does not enforce transitive or symmetric spatial constraints.

### Future Scope & Unsolved Frontiers
Constraint-guided decoding for spatial consistency.

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `3 / 5` — *Moderate Diagnostic Prior*

### Relevance Rationale
Directly explains the erratic spatial scores observed in our RwR baseline.

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **Consistency Metric**: Quantifies internal logical contradiction on inverse spatial queries.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **Model Solution**: Diagnostic audit only.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: Spatial consistency probing.
- **How our inquiry differs**: Our programmatic routing framework enforces mathematical symmetry and transitivity by construction.

---

## 8. Technical Deep-Dive & Architecture Specification

```mermaid
flowchart LR
    A[Visual Input] --> B[Encoder: Evaluates 10 MLLMs]
    B --> C[Projector: Native]
    C --> D[LLM Backbone: Various]
    D --> E[Predictions: Native]
```

- **Vision Encoder**: `Evaluates 10 MLLMs`
- **Cross-Modal Projector**: `Native`
- **Language Backbone**: `Various`
- **Visual Token Budget**: `Native`

---

## 9. Actionable Takeaways for Our Codebase & Experiments
- [ ] **Consistency Check**: Test our proposed model on inverse spatial queries to prove zero contradiction rate.
- [ ] **Paper Metric**: Report spatial consistency rate alongside raw accuracy.
