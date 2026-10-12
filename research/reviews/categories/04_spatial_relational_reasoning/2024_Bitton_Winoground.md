# Paper Review: Beyond Winoground: Probing Spatial Prepositions and Compositionality in VLMs

| Field | Details |
| :--- | :--- |
| **Authors** | Yonatan Bitton, Hadas Orgad, Pradeep Dasigi, Gabriel Stanovsky, Roy Schwartz |
| **Institution(s)** | Hebrew University of Jerusalem, Allen Institute for AI (AI2) |
| **Publication Date / Venue** | 2024 / ACL 2024 |
| **arXiv ID / Link** | [2403.07840](https://arxiv.org/abs/2403.07840) |
| **Code Repository** | [https://github.com/yonatanbitton/beyond-winoground](https://github.com/yonatanbitton/beyond-winoground) |
| **Category** | Spatial & Relational Reasoning in VLMs |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
Probes compositional understanding of spatial prepositions ('above', 'below', 'next to', 'inside') using counterfactual image-text pairs, proving models behave like bag-of-words.

---

## 2. Abstract
> "We evaluate whether vision-language models truly understand spatial prepositions or merely rely on lexical frequencies. Using carefully balanced minimal pairs where swapping prepositions reverses ground truth, we demonstrate that most VLMs exhibit near-chance compositional accuracy."

---

## 3. Key Findings
1. Swapping spatial prepositions drops VLM accuracy to 28.5% (chance = 25%).
2. Attention maps show models ignore preposition tokens during visual cross-attention.
3. Pretrained representations do not bind spatial relation words to physical visual geometry.

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
Vision-language alignment is heavily biased toward nouns and attributes, treating prepositions as ungrounded noise.

### Future Scope & Unsolved Frontiers
Compositional contrastive pretraining.

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `3 / 5` — *Moderate Linguistic Prior*

### Relevance Rationale
Linguistic explanation for why spatial relation queries fail across VLMs.

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **Minimal Pair Probing**: Proves models treat spatial prepositions as bag-of-words.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **Visual Architecture Solution**: Diagnostic linguistics paper.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: Linguistic probing of spatial compositionality.
- **How our inquiry differs**: We tackle the visual perception and spatial grounding pipeline in remote sensing.

---

## 8. Technical Deep-Dive & Architecture Specification

```mermaid
flowchart LR
    A[Visual Input] --> B[Encoder: CLIP ViT-B/32 & ViT-L/14]
    B --> C[Projector: Linear]
    C --> D[LLM Backbone: None (Contrastive scoring)]
    D --> E[Predictions: N/A]
```

- **Vision Encoder**: `CLIP ViT-B/32 & ViT-L/14`
- **Cross-Modal Projector**: `Linear`
- **Language Backbone**: `None (Contrastive scoring)`
- **Visual Token Budget**: `N/A`

---

## 9. Actionable Takeaways for Our Codebase & Experiments
- [ ] **Language Finding**: Do not expect text prompts alone to enforce spatial preposition understanding.
