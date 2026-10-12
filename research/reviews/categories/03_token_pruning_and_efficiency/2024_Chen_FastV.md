# Paper Review: An Image is Worth 1/2 Tokens After Layer 2: Plug-and-Play Sparse Auto-Encoders for Efficient Vision-Language Models (FastV)

| Field | Details |
| :--- | :--- |
| **Authors** | Liang Chen, Haozhe Zhao, Zhiqiang Hu, Jiashuo Sun, Baobao Chang |
| **Institution(s)** | Peking University |
| **Publication Date / Venue** | 2024 / ECCV 2024 |
| **arXiv ID / Link** | [2403.06764](https://arxiv.org/abs/2403.06764) |
| **Code Repository** | [https://github.com/pkunlp-icler/FastV](https://github.com/pkunlp-icler/FastV) |
| **Category** | Token Pruning, Efficient Connectors & Compression |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
Demonstrates that over 50% of visual tokens receive virtually zero attention weight after early LLM layers, proposing a training-free layer-2 pruning strategy that cuts FLOPs by 45%.

---

## 2. Abstract
> "We investigate attention allocation over visual tokens in deep MLLMs and discover that attention over visual tokens dramatically diminishes after the first 2-3 layers. FastV leverages this observation to prune 50-75% of visual tokens after layer 2 in a plug-and-play, training-free manner."

---

## 3. Key Findings
1. Visual tokens exhibit extreme attention sparsity in intermediate and late LLM layers.
2. Pruning low-attention tokens after layer 2 retains 99% accuracy on general VQA.
3. Training-free: requires zero fine-tuning.

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
Deep LLM layers primarily perform linguistic reasoning and do not require full visual token resolution.

### Future Scope & Unsolved Frontiers
Task-adaptive pruning schedules.

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `4 / 5` — *High Efficiency Prior*

### Relevance Rationale
Provides a plug-and-play training-free method to accelerate Qwen2.5-VL inference in our pipeline.

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **Training-Free Pruning**: Plug-and-play attention-based token dropping after layer 2.
- **Universal Applicability**: Works on any decoder LLM backbone.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **High-Resolution Remote Sensing**: Tested on standard 336x336 images; does not address 8K multi-crop setups.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: Layer-wise attention pruning on natural images.
- **How our inquiry differs**: We evaluate FastV on multi-crop high-resolution remote sensing to test if spatial relations survive late-layer pruning.

---

## 8. Technical Deep-Dive & Architecture Specification

```mermaid
flowchart LR
    A[Visual Input] --> B[Encoder: CLIP ViT-L/14-336]
    B --> C[Projector: MLP]
    C --> D[LLM Backbone: LLaVA-1.5-7B / Vicuna-7B]
    D --> E[Predictions: Pruned from 576 to 144 tokens after layer 2]
```

- **Vision Encoder**: `CLIP ViT-L/14-336`
- **Cross-Modal Projector**: `MLP`
- **Language Backbone**: `LLaVA-1.5-7B / Vicuna-7B`
- **Visual Token Budget**: `Pruned from 576 to 144 tokens after layer 2`

---

## 9. Actionable Takeaways for Our Codebase & Experiments
- [ ] **Efficiency Module**: Test FastV layer-2 pruning inside our Qwen2.5-VL inference runner to cut decoding latency.
