# Paper Review: RelationalVLM: Explicit Spatial Relations via Positional Encodings

| Field | Details |
| :--- | :--- |
| **Authors** | Hao Yuan, Jianfei Gao, Siyuan Li |
| **Institution(s)** | Tsinghua University |
| **Publication Date / Venue** | 2024 / NeurIPS 2024 |
| **arXiv ID / Link** | [2408.15234](https://arxiv.org/abs/2408.15234) |
| **Code Repository** | [https://github.com/YuanHao/RelationalVLM](https://github.com/YuanHao/RelationalVLM) |
| **Category** | Spatial & Relational Reasoning in VLMs |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
Injects explicit relative position embeddings between visual tokens and text entities to encode directional vectors directly into self-attention layers.

---

## 2. Abstract
> "Vision-language models rely on 1D or basic 2D positional encodings that fail to represent directional vectors between entities. RelationalVLM introduces Relative Spatial Position Encoding (RSPE), directly modulating attention logits by relative displacement vectors."

---

## 3. Key Findings
1. RSPE improves spatial relation accuracy by +14.6% on CLEVR and GQA.
2. Preserves cardinal orientation under rotation.
3. Modulates self-attention weights directly with Euclidean displacement vectors.

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
Directly encoding pairwise displacement vectors into self-attention eliminates spatial disorientation.

### Future Scope & Unsolved Frontiers
Extending to multi-crop tiled inputs.

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `4 / 5` — *High Architectural Prior*

### Relevance Rationale
Provides the architectural blueprint for why relative coordinate embeddings fix spatial reasoning.

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **Relative Spatial Position Encoding**: Modulates attention logits by 2D displacement vectors $\Delta x, \Delta y$.
- **Directional Invariance**: Explicit representation of relative angles and distances.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **Training-Free Inference**: Requires retraining attention layers with RSPE bias.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: Relative positional encoding for spatial reasoning.
- **How our inquiry differs**: We design prompt-level and programmatic solutions that work training-free on frozen models.

---

## 8. Technical Deep-Dive & Architecture Specification

```mermaid
flowchart LR
    A[Visual Input] --> B[Encoder: ViT-L/14 with RSPE Attention]
    B --> C[Projector: MLP]
    C --> D[LLM Backbone: Vicuna-7B]
    D --> E[Predictions: 576 tokens]
```

- **Vision Encoder**: `ViT-L/14 with RSPE Attention`
- **Cross-Modal Projector**: `MLP`
- **Language Backbone**: `Vicuna-7B`
- **Visual Token Budget**: `576 tokens`

---

## 9. Actionable Takeaways for Our Codebase & Experiments
- [ ] **Architectural Principle**: Spatial relations depend on relative displacement vectors $(\Delta x, \Delta y)$.
