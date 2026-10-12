# Paper Review: InstructBLIP: Towards General-purpose Vision-Language Models with Instruction Tuning

| Field | Details |
| :--- | :--- |
| **Authors** | Wenliang Dai, Junnan Li, Dongxu Li, Anthony Meng Huat Tiong, Junqi Zhao, Weisheng Wang, Boyang Li, Pascale Fung, Steven Hoi |
| **Institution(s)** | Salesforce Research |
| **Publication Date / Venue** | 2023 / NeurIPS 2023 |
| **arXiv ID / Link** | [2305.06500](https://arxiv.org/abs/2305.06500) |
| **Code Repository** | [https://github.com/salesforce/LAVIS](https://github.com/salesforce/LAVIS) |
| **Category** | Token Pruning, Efficient Connectors & Compression |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
Introduces instruction-aware visual feature extraction via an instruction-guided Q-Former, extracting 32 query-tailored visual tokens from dense image grids.

---

## 2. Abstract
> "We present InstructBLIP, introducing instruction-aware visual feature extraction. By feeding the user instruction into the Q-Former alongside learnable queries, InstructBLIP extracts 32 task-specific visual tokens that adapt dynamically to the query objective."

---

## 3. Key Findings
1. Instruction-guided queries extract task-relevant features better than instruction-agnostic resamplers.
2. Generates a compact fixed budget of 32 visual tokens.
3. Compression to 32 tokens discards fine spatial coordinates and background anchors.

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
Instruction conditioning makes token abstractors flexible, but extreme compression impairs spatial localization.

### Future Scope & Unsolved Frontiers
Scaling query token count for complex scenes.

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `4 / 5` — *Foundational Q-Former Prior*

### Relevance Rationale
Exemplifies instruction-guided query abstractors; demonstrates the resolution vs abstraction trade-off.

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **Instruction-Guided Q-Former**: Conditioning visual queries on user text instructions.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **Spatial Localization**: 32 tokens cannot represent 100+ small aerial objects or spatial distances.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: Foundational Q-Former baseline.
- **How our inquiry differs**: We preserve spatial coordinate structures rather than collapsing everything into 32 semantic tokens.

---

## 8. Technical Deep-Dive & Architecture Specification

```mermaid
flowchart LR
    A[Visual Input] --> B[Encoder: EVA-CLIP ViT-g/14]
    B --> C[Projector: Instruction-guided Q-Former (32 tokens)]
    C --> D[LLM Backbone: Flan-T5-XXL / Vicuna-7B]
    D --> E[Predictions: Fixed 32 tokens]
```

- **Vision Encoder**: `EVA-CLIP ViT-g/14`
- **Cross-Modal Projector**: `Instruction-guided Q-Former (32 tokens)`
- **Language Backbone**: `Flan-T5-XXL / Vicuna-7B`
- **Visual Token Budget**: `Fixed 32 tokens`

---

## 9. Actionable Takeaways for Our Codebase & Experiments
- [ ] **Abstractor Limitation**: Do NOT use low-token Q-Formers (<64 tokens) for spatial reasoning tasks.
