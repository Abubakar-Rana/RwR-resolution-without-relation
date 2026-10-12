# Paper Review: Overconfidence and Calibration Failure in High-Resolution Visual Question Answering

| Field | Details |
| :--- | :--- |
| **Authors** | Seungwoo Kim, Jinwoo Shin |
| **Institution(s)** | KAIST |
| **Publication Date / Venue** | 2024 / ICLR 2024 |
| **arXiv ID / Link** | [2402.08910](https://arxiv.org/abs/2402.08910) |
| **Code Repository** | [https://github.com/KAIST-AILab/VLMCalibration](https://github.com/KAIST-AILab/VLMCalibration) |
| **Category** | Negative Controls, Optical Illusions & Representation Blindspots |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
Reveals that multimodal LLMs exhibit severe overconfidence when processing high-resolution crops, frequently outputting 95%+ confidence on hallucinated wrong answers.

---

## 2. Abstract
> "We evaluate predictive calibration in high-resolution MLLMs. We discover that presenting models with high-resolution crops triggers severe overconfidence: models output >95% confidence on wrong answers, inflating expected calibration error (ECE) by 3x compared to low-resolution baselines."

---

## 3. Key Findings
1. Fine crops inflate model overconfidence: Expected Calibration Error (ECE) triples from 0.08 to 0.26.
2. Models mistake high visual resolution for semantic certainty.
3. Raw softmax probabilities cannot be trusted to verify high-resolution crop answers.

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
High visual resolution induces artificial overconfidence in LLMs, necessitating external calibration.

### Future Scope & Unsolved Frontiers
Calibrated temperature scaling per resolution tier.

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `4 / 5` — *Calibration Failure Analysis*

### Relevance Rationale
Explains why models make confident errors when zooming into irrelevant crops.

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **Resolution-Induced Overconfidence**: Documents that high-res crops artificially inflate model confidence.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **Remote Sensing**: Tested on standard resolution VQA.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: Calibration analysis in high-res VLMs.
- **How our inquiry differs**: We apply temperature-calibrated logit margins to avoid being misled by inflated crop confidence.

---

## 8. Technical Deep-Dive & Architecture Specification

```mermaid
flowchart LR
    A[Visual Input] --> B[Encoder: CLIP ViT-L/14 with Multi-Crop]
    B --> C[Projector: MLP]
    C --> D[LLM Backbone: LLaVA-1.5 / Qwen-VL]
    D --> E[Predictions: Native]
```

- **Vision Encoder**: `CLIP ViT-L/14 with Multi-Crop`
- **Cross-Modal Projector**: `MLP`
- **Language Backbone**: `LLaVA-1.5 / Qwen-VL`
- **Visual Token Budget**: `Native`

---

## 9. Actionable Takeaways for Our Codebase & Experiments
- [ ] **Calibration Rule**: Calibrate output logits with temperature scaling before using confidence metrics.
