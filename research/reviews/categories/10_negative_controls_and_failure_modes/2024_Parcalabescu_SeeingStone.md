# Paper Review: Seeing Stone: Measuring Relational Misalignment in Multi-Modal Models

| Field | Details |
| :--- | :--- |
| **Authors** | Letitia Parcalabescu, Michele Cafagna, Lilitta Muradjan, Anette Frank, Iacer Calixto, Albert Gatt |
| **Institution(s)** | Heidelberg University, University of Malta, Amsterdam UMC |
| **Publication Date / Venue** | 2022 / EMNLP 2022 |
| **arXiv ID / Link** | [2112.05147](https://arxiv.org/abs/2112.05147) |
| **Code Repository** | [https://github.com/Letitia-P/aro](https://github.com/Letitia-P/aro) |
| **Category** | Negative Controls, Optical Illusions & Representation Blindspots |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
Introduces the VSR (Visual Spatial Reasoning) benchmark and audits relational alignment, showing models fail to distinguish 'to the left of' from 'to the right of' in 50% of trials.

---

## 2. Abstract
> "We evaluate relational spatial understanding in 20 multimodal models. We show that models exhibit severe relational misalignment: while they recognize the entities involved, they fail to verify spatial relations above random chance."

---

## 3. Key Findings
1. Models score 52.3% on binary spatial relation verification (random chance is 50.0%).
2. Left/right and front/behind relations are completely unaligned in visual token space.
3. Object recognition accuracy does not correlate with relational accuracy.

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
Object recognition capability is completely decoupled from spatial relational reasoning capability.

### Future Scope & Unsolved Frontiers
Spatially grounded pretraining.

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `4 / 5` — *Diagnostic Failure Analysis*

### Relevance Rationale
Directly supports our crossover finding: high perception accuracy does NOT translate to spatial relational reasoning.

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **Decoupling of Perception and Relation**: Rigorous proof that recognizing objects does not confer spatial relational reasoning.
- **VSR Diagnostic Suite**: Standardized spatial relation minimal pairs.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **Architecture Fix**: Diagnostic audit only.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: Relational spatial alignment audit.
- **How our inquiry differs**: We document how tile selection active zoom actively WORSENS this relational deficit.

---

## 8. Technical Deep-Dive & Architecture Specification

```mermaid
flowchart LR
    A[Visual Input] --> B[Encoder: CLIP, FLAVA, ViLT, ALBEF]
    B --> C[Projector: Native]
    C --> D[LLM Backbone: None (Pre-LLM era)]
    D --> E[Predictions: Native]
```

- **Vision Encoder**: `CLIP, FLAVA, ViLT, ALBEF`
- **Cross-Modal Projector**: `Native`
- **Language Backbone**: `None (Pre-LLM era)`
- **Visual Token Budget**: `Native`

---

## 9. Actionable Takeaways for Our Codebase & Experiments
- [ ] **Paper Defense**: Cite Parcalabescu et al. to prove that perception and relation are fundamentally decoupled in multimodal models.
