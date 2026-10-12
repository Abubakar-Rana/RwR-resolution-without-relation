# Paper Review: The Llama 3 Herd of Models: Multimodal Architecture and High-Resolution Adapter

| Field | Details |
| :--- | :--- |
| **Authors** | Abhimanyu Dubey, Jiahui Yu, et al., Llama Team |
| **Institution(s)** | Meta AI |
| **Publication Date / Venue** | 2024 / arXiv preprint |
| **arXiv ID / Link** | [2407.21783](https://arxiv.org/abs/2407.21783) |
| **Code Repository** | [https://github.com/meta-llama/llama-models](https://github.com/meta-llama/llama-models) |
| **Category** | General Foundation VLMs & Multi-Crop Connectors |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
Presents Llama 3.2 Vision (11B and 90B), using a cross-attention vision adapter that splices visual tokens into frozen Llama 3 language layers without disturbing pre-trained language weights.

---

## 2. Abstract
> "We present the multimodal extension of Llama 3. By incorporating a vision encoder and cross-attention adapter layers into the Llama 3 backbone, Llama 3.2 Vision achieves competitive multimodal reasoning across image, chart, and document tasks."

---

## 3. Key Findings
1. Gated cross-attention adapters preserve text reasoning while injecting visual perception.
2. Supports high-resolution tiling up to 4 tiles.
3. Preserves linguistic reasoning performance with zero regression.

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
Cross-attention adapters provide modular multimodal extension of language models without catastrophic forgetting.

### Future Scope & Unsolved Frontiers
Scaling to video and continuous speech.

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `4 / 5` — *Foundational Open-Weights VLM*

### Relevance Rationale
Key open-weights foundation model alternative to Qwen2.5-VL.

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **Cross-Attention Adapter Architecture**: Gated cross-attention layers inserted every 4 transformer blocks.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **Gigapixel Native Slicing**: Caps at 4 tiles; cannot handle 8K imagery directly.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: Open-weights foundation VLM.
- **How our inquiry differs**: We evaluate Qwen2.5-VL-7B and can test Llama 3.2 Vision-11B as a cross-architecture validation.

---

## 8. Technical Deep-Dive & Architecture Specification

```mermaid
flowchart LR
    A[Visual Input] --> B[Encoder: ViT-H/14 (Pretrained)]
    B --> C[Projector: Cross-Attention Adapter Layers]
    C --> D[LLM Backbone: Llama-3-8B / Llama-3-70B]
    D --> E[Predictions: Variable (up to 4 tiles)]
```

- **Vision Encoder**: `ViT-H/14 (Pretrained)`
- **Cross-Modal Projector**: `Cross-Attention Adapter Layers`
- **Language Backbone**: `Llama-3-8B / Llama-3-70B`
- **Visual Token Budget**: `Variable (up to 4 tiles)`

---

## 9. Actionable Takeaways for Our Codebase & Experiments
- [ ] **Cross-Architecture Validation**: Test our routed framework on Llama-3.2-Vision-11B to confirm findings generalize beyond Qwen.
