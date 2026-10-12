# Paper Review: Speculative Decoding for Multimodal Language Models

| Field | Details |
| :--- | :--- |
| **Authors** | Junhyuk Park, Sangmin Bae |
| **Institution(s)** | KAIST |
| **Publication Date / Venue** | 2024 / EMNLP 2024 |
| **arXiv ID / Link** | [2404.14890](https://arxiv.org/abs/2404.14890) |
| **Code Repository** | [https://github.com/KAIST-AILab/SpeculativeMLLM](https://github.com/KAIST-AILab/SpeculativeMLLM) |
| **Category** | Dynamic Routing, Multi-Resolution & Cascaded VLM Systems |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
Implements speculative decoding across model parameter sizes in multimodal LLMs, using a 1B vision-language model to draft tokens for a 7B target model.

---

## 2. Abstract
> "We explore speculative decoding in vision-language models. Using a 1B MLLM as a draft model and a 7B MLLM as target verifier, SpeculativeMLLM achieves a 2.1x wall-clock inference speedup with zero degradation in benchmark accuracy."

---

## 3. Key Findings
1. Draft acceptance rate exceeds 75% on visual question answering.
2. 2.1x wall-clock speedup without modifying output distributions.
3. Requires both draft and target models to share identical tokenizers.

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
Speculative decoding delivers lossless throughput acceleration across multimodal language models.

### Future Scope & Unsolved Frontiers
Multi-draft speculative pipelines.

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `3 / 5` — *Moderate Efficiency Prior*

### Relevance Rationale
Provides complementary inference acceleration for our evaluation runner.

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **Cross-Model Speculative Decoding**: Lossless 2.1x speedup using 1B draft model.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **Routing Logic**: Focuses on text decoding acceleration; does not solve visual crop selection.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: Speculative decoding implementation.
- **How our inquiry differs**: We focus on the visual routing and crop selection dilemma.

---

## 8. Technical Deep-Dive & Architecture Specification

```mermaid
flowchart LR
    A[Visual Input] --> B[Encoder: SigLIP-SO400M]
    B --> C[Projector: MLP]
    C --> D[LLM Backbone: Draft: TinyLLaVA-1B / Target: Qwen2-VL-7B]
    D --> E[Predictions: Native]
```

- **Vision Encoder**: `SigLIP-SO400M`
- **Cross-Modal Projector**: `MLP`
- **Language Backbone**: `Draft: TinyLLaVA-1B / Target: Qwen2-VL-7B`
- **Visual Token Budget**: `Native`

---

## 9. Actionable Takeaways for Our Codebase & Experiments
- [ ] **Serving Tip**: Use speculative decoding if evaluating all 45K items of XLRS-Bench.
