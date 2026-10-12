# Paper Review: Monkey: Image Resolution and Text Label Are Important Things for Large Multi-Modal Models

| Field | Details |
| :--- | :--- |
| **Authors** | Zhang Li, Biao Yang, Qiang Liu, Zhiyin Ma, Shuo Zhang, Jingxu Yang, Yabo Sun, Yuliang Liu, Xiang Bai |
| **Institution(s)** | Huazhong University of Science and Technology |
| **Publication Date / Venue** | 2024 / CVPR 2024 |
| **arXiv ID / Link** | [2311.06607](https://arxiv.org/abs/2311.06607) |
| **Code Repository** | [https://github.com/Yuliang-Liu/Monkey](https://github.com/Yuliang-Liu/Monkey) |
| **Category** | Active Zoom, Guided Visual Search & Dynamic Tiling |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
Monkey scales input resolution to 1344x896 without pretraining from scratch by dividing the image into uniform patches and aggregating features with a cross-patch visual resampler.

---

## 2. Abstract
> "We present Monkey, a training-efficient approach scaling MLLM input resolution. By dividing images into uniform patches and processing each through a pre-trained visual encoder before cross-patch fusion, Monkey enhances fine text and small object detection."

---

## 3. Key Findings
1. Scaling resolution directly boosts fine-grained perception (+15.2% on document and dense QA).
2. Cross-patch resampler prevents token explosion.
3. Dense uniform patching scales quadratically with gigapixel image dimensions.

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
Resolution scaling is the single most effective lever for small target perception.

### Future Scope & Unsolved Frontiers
Non-uniform adaptive patching.

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `4 / 5` — *High Architectural Prior*

### Relevance Rationale
Demonstrates why resolution scaling boosts small object perception.

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **Resolution Scaling**: Practical recipe for scaling resolution on pretrained VLMs.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **Adaptive Selection**: Applies uniform dense patching, failing to scale to 8K imagery.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: Uniform patching recipe on natural images; does not scale to 8K imagery.
- **How our inquiry differs**: We use selective tile selection and routing rather than uniform dense patching.

---

## 8. Technical Deep-Dive & Architecture Specification

```mermaid
flowchart LR
    A[Visual Input] --> B[Encoder: CLIP ViT-BigG]
    B --> C[Projector: Multi-level Resampler]
    C --> D[LLM Backbone: Qwen-7B]
    D --> E[Predictions: 1,024 tokens]
```

- **Vision Encoder**: `CLIP ViT-BigG`
- **Cross-Modal Projector**: `Multi-level Resampler`
- **Language Backbone**: `Qwen-7B`
- **Visual Token Budget**: `1,024 tokens`

---

## 9. Actionable Takeaways for Our Codebase & Experiments
- [ ] **Perception Gains**: Confirms resolution boosts perception; reinforces why RwR saw +4.1 pp on perception.
