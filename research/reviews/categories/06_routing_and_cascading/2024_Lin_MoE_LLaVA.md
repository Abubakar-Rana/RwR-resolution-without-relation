# Paper Review: MoE-LLaVA: Mixture of Experts for Large Vision-Language Models

| Field | Details |
| :--- | :--- |
| **Authors** | Bin Lin, Zhenyu Tang, Yang Ye, Jiaxi Cui, Bin Zhu, Peng Jin, Junwu Zhang, Munan Ning, Li Yuan |
| **Institution(s)** | Peking University, Peng Cheng Laboratory |
| **Publication Date / Venue** | 2024 / arXiv preprint |
| **arXiv ID / Link** | [2401.15947](https://arxiv.org/abs/2401.15947) |
| **Code Repository** | [https://github.com/PKU-YuanGroup/MoE-LLaVA](https://github.com/PKU-YuanGroup/MoE-LLaVA) |
| **Category** | Dynamic Routing, Multi-Resolution & Cascaded VLM Systems |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
Adapts Sparse Mixture of Experts (MoE) to multimodal LLMs, routing tokens to specialized visual and linguistic expert networks to achieve 13B performance with only 3B activated parameters.

---

## 2. Abstract
> "We present MoE-LLaVA, a sparse mixture-of-experts architecture for multimodal LLMs. By replacing standard feed-forward networks with sparse MoE layers, MoE-LLaVA dynamically activates only top-k experts per token, scaling model capacity with constant compute."

---

## 3. Key Findings
1. Sparse MoE activates only 2.2B to 3.0B parameters per token, reducing inference latency by 3x.
2. Discovers expert specialization: distinct experts specialize in visual geometry vs linguistic semantics.
3. Routing tokens through specialized visual experts improves fine-grained grounding.

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
Sparse routing across specialized expert networks scales multimodal capacity without increasing inference cost.

### Future Scope & Unsolved Frontiers
Routing at the sequence level and resolution level.

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `4 / 5` — *High Architectural Prior*

### Relevance Rationale
Validates that sparse conditional routing is more efficient and accurate than uniform monolithic computation.

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **Sparse MoE for VLMs**: Top-k sparse routing inside multimodal LLM feed-forward layers.
- **Expert Specialization**: Visual experts specialize in spatial layout vs semantic recognition.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **Pipeline-Level Routing**: Operates inside FFN layers during training; requires pretraining from scratch.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: Token-level MoE inside transformer layers.
- **How our inquiry differs**: We operate at the pipeline/system level, routing entire queries to different inference pipelines without model retraining.

---

## 8. Technical Deep-Dive & Architecture Specification

```mermaid
flowchart LR
    A[Visual Input] --> B[Encoder: CLIP ViT-L/14-336]
    B --> C[Projector: MLP]
    C --> D[LLM Backbone: MoE-LLaVA (16 experts, top-2 activated)]
    D --> E[Predictions: 576 tokens]
```

- **Vision Encoder**: `CLIP ViT-L/14-336`
- **Cross-Modal Projector**: `MLP`
- **Language Backbone**: `MoE-LLaVA (16 experts, top-2 activated)`
- **Visual Token Budget**: `576 tokens`

---

## 9. Actionable Takeaways for Our Codebase & Experiments
- [ ] **Routing Inspiration**: Spatial and semantic tasks naturally activate distinct pathways; pipeline routing mirrors this split.
