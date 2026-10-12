# Paper Review: Visual Programming: Compositional Visual Reasoning Without Training

| Field | Details |
| :--- | :--- |
| **Authors** | Tanmay Gupta, Aniruddha Kembhavi |
| **Institution(s)** | Allen Institute for AI (AI2) |
| **Publication Date / Venue** | 2023 / CVPR 2023 |
| **arXiv ID / Link** | [2211.11559](https://arxiv.org/abs/2211.11559) |
| **Code Repository** | [https://github.com/allenai/visprog](https://github.com/allenai/visprog) |
| **Category** | Spatial & Relational Reasoning in VLMs |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
Introduces Visual Programming (VisProg), using in-context learning in LLMs to generate modular visual programs that execute step-by-step visual reasoning (crop, detect, filter, count).

---

## 2. Abstract
> "We present VisProg, a neuro-symbolic approach to complex and compositional visual tasks without task-specific training. VisProg prompts an LLM to generate 2-step Python-like visual programs that invoke CV models, image filters, and geometric calculations."

---

## 3. Key Findings
1. In-context program generation achieves SOTA on compositional visual reasoning (GQA, NLVR2).
2. Step-by-step execution provides complete interpretability.
3. Failures are easily debugged to either program generation or specific vision tool errors.

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
Neuro-symbolic program synthesis sidesteps the reasoning limitations of monolithic vision-language transformers.

### Future Scope & Unsolved Frontiers
Dynamic replanning upon tool execution failure.

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `4 / 5` — *High Programmatic Prior*

### Relevance Rationale
Validates the programmatic decomposition of complex multi-step aerial queries.

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **Visual Program Generation**: In-context prompts generating interpretable vision program steps.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **Aerial Remote Sensing Context**: Tested on natural web images; tools lack aerial domain priors.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: Neuro-symbolic program generation.
- **How our inquiry differs**: We tailor program steps specifically for gigapixel aerial operations (tile crop, orient detect, count).

---

## 8. Technical Deep-Dive & Architecture Specification

```mermaid
flowchart LR
    A[Visual Input] --> B[Encoder: ViLD / MDETR / OpenCV]
    B --> C[Projector: Tool interfaces]
    C --> D[LLM Backbone: GPT-3 (text-davinci-003)]
    D --> E[Predictions: N/A]
```

- **Vision Encoder**: `ViLD / MDETR / OpenCV`
- **Cross-Modal Projector**: `Tool interfaces`
- **Language Backbone**: `GPT-3 (text-davinci-003)`
- **Visual Token Budget**: `N/A`

---

## 9. Actionable Takeaways for Our Codebase & Experiments
- [ ] **Program Template**: Use 3-shot in-context examples to generate aerial spatial programs.
