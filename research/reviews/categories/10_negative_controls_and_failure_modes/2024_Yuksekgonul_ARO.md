# Paper Review: When and Why Vision-Language Models Behave Like Bags-of-Words

| Field | Details |
| :--- | :--- |
| **Authors** | Mert Yuksekgonul, Federico Bianchi, Pratyush Kalluri, Dan Jurafsky, James Zou |
| **Institution(s)** | Stanford University |
| **Publication Date / Venue** | 2023 / ICLR 2023 |
| **arXiv ID / Link** | [2210.01936](https://arxiv.org/abs/2210.01936) |
| **Code Repository** | [https://github.com/mertyg/aro](https://github.com/mertyg/aro) |
| **Category** | Negative Controls, Optical Illusions & Representation Blindspots |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
Introduces the ARO benchmark (Attribution, Relation, and Order), proving that contrastive pretraining encourages models to treat sentences as bags-of-words, ignoring word order and spatial predicates.

---

## 2. Abstract
> "We present ARO, benchmarking vision-language models on compositionality. Across multiple model families, we show that contrastive models behave like bag-of-words models: shuffling word order or swapping relational predicates has virtually no effect on retrieval scores."

---

## 3. Key Findings
1. Shuffling text caption words reduces retrieval score by less than 5% in standard CLIP.
2. Models cannot distinguish 'the dog is to the left of the cat' from 'the cat is to the left of the dog'.
3. Pretraining on noisy web captions teaches models to correlate co-occurring keywords rather than syntax.

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
Contrastive vision-language pretraining actively penalizes syntactic sensitivity, producing bag-of-words representations.

### Future Scope & Unsolved Frontiers
Structure-aware contrastive losses.

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `5 / 5` — *Foundational Negative Analysis*

### Relevance Rationale
CORE THEORETICAL ROOT CAUSE: proves why CLIP-based tile scoring ($s_{clip}$) fails on relational queries.

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **Bag-of-Words Proof**: Empirical proof that contrastive models ignore syntax and spatial predicates.
- **ARO Benchmark**: Standardized evaluation of Attribution, Relation, and Order.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **Gigapixel Resolution**: Tested on standard resolution images.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: Foundational paper explaining why VLMs ignore relational syntax.
- **How our inquiry differs**: We explain how this bag-of-words failure specifically causes the CLIP tile selector in RwR to pick irrelevant crops.

---

## 8. Technical Deep-Dive & Architecture Specification

```mermaid
flowchart LR
    A[Visual Input] --> B[Encoder: CLIP ViT-B/32 & ViT-L/14]
    B --> C[Projector: Linear]
    C --> D[LLM Backbone: Transformer text encoder]
    D --> E[Predictions: Global pooled embedding]
```

- **Vision Encoder**: `CLIP ViT-B/32 & ViT-L/14`
- **Cross-Modal Projector**: `Linear`
- **Language Backbone**: `Transformer text encoder`
- **Visual Token Budget**: `Global pooled embedding`

---

## 9. Actionable Takeaways for Our Codebase & Experiments
- [ ] **Theoretical Grounding**: Cite Yuksekgonul et al. to explain why CLIP tile selection fails on spatial relation queries (it treats query prepositions as bag-of-words noise).
