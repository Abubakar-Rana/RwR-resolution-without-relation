# Paper Review: Divide, Conquer and Combine: A Training-Free Framework for High-Resolution Image Perception in Multimodal Large Language Models

| Field | Details |
| :--- | :--- |
| **Authors** | Weixian Wang, Zhangwei Gao, Mengmeng Wang, Shenghao Zhang |
| **Institution(s)** | Zhejiang University |
| **Publication Date / Venue** | 2025 / CVPR 2025 |
| **arXiv ID / Link** | [2408.01890](https://arxiv.org/abs/2408.01890) |
| **Code Repository** | [https://github.com/ZJU-VIP/DC2](https://github.com/ZJU-VIP/DC2) |
| **Category** | Active Zoom, Guided Visual Search & Dynamic Tiling |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
DC2 divides high-resolution images into patches, evaluates each patch independently with the VLM, and aggregates local answers with a global combiner without requiring model retraining.

---

## 2. Abstract
> "We introduce DC2 (Divide, Conquer, Combine), a training-free framework scaling off-the-shelf MLLMs to ultra-high resolution. DC2 partitions the image, conquer patches via query-guided filtering, and combines intermediate predictions into the final output."

---

## 3. Key Findings
1. Training-free patching improves detail detection on standard MLLMs.
2. Combining local patch descriptions often fails on spatial relational questions.
3. When objects cross patch seams, the combine step hallucinates duplicates.

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
Late-fusion combination of patch text outputs cannot reconstruct spatial geometry.

### Future Scope & Unsolved Frontiers
Early visual token fusion rather than late text combination.

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `4 / 5` — *High Algorithmic Relevance*

### Relevance Rationale
Demonstrates why text-level late combination fails on spatial geometry.

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **Training-Free Pipeline**: No fine-tuning required; wraps any existing VLM.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **Seam Artifact Fix**: Duplicate objects generated when targets intersect patch seams.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: Uses late text combination; our baseline proves text combination fails on relations.
- **How our inquiry differs**: We avoid late text combination; we feed visual crops directly to the multimodal LLM.

---

## 8. Technical Deep-Dive & Architecture Specification

```mermaid
flowchart LR
    A[Visual Input] --> B[Encoder: CLIP / Qwen-VL native encoder]
    B --> C[Projector: Native]
    C --> D[LLM Backbone: GPT-4V / Qwen2-VL]
    D --> E[Predictions: Native]
```

- **Vision Encoder**: `CLIP / Qwen-VL native encoder`
- **Cross-Modal Projector**: `Native`
- **Language Backbone**: `GPT-4V / Qwen2-VL`
- **Visual Token Budget**: `Native`

---

## 9. Actionable Takeaways for Our Codebase & Experiments
- [ ] **Pitfall Caution**: Never use late text aggregation for spatial counting or cardinal relations.
