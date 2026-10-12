# Paper Review: Confidence-Calibrated Routing for Cost-Efficient Multi-LLM Serving

| Field | Details |
| :--- | :--- |
| **Authors** | Zhuang Liu, Shengbang Tong, Yi Ma |
| **Institution(s)** | UC Berkeley |
| **Publication Date / Venue** | 2024 / ICML 2024 |
| **arXiv ID / Link** | [2405.02110](https://arxiv.org/abs/2405.02110) |
| **Code Repository** | [https://github.com/CalibratedRouting/CalibratedRoute](https://github.com/CalibratedRouting/CalibratedRoute) |
| **Category** | Dynamic Routing, Multi-Resolution & Cascaded VLM Systems |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
Calibrates output probabilities using temperature scaling and conformal prediction to ensure routers only trust high-confidence predictions, preventing routing errors.

---

## 2. Abstract
> "Uncalibrated language model logits lead to poor routing decisions in multi-model serving. We introduce Confidence-Calibrated Routing, applying conformal prediction to establish rigorous confidence guarantees before deciding whether to accept a fast model's output or escalate to a heavy model."

---

## 3. Key Findings
1. Raw softmax probabilities are systematically overconfident in modern LLMs.
2. Temperature scaling and conformal calibration restore predictive calibration.
3. Calibrated routing reduces misclassification by 34% compared to raw argmax gating.

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
Probability calibration is mandatory for robust threshold-based escalation in cascaded model serving.

### Future Scope & Unsolved Frontiers
Multimodal calibrated routing.

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `4 / 5` — *High Routing Prior*

### Relevance Rationale
CRITICAL FOR CASCADED ROUTING: ensures our logit margin threshold $\tau$ is calibrated and statistically grounded.

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **Conformal Calibration**: Rigorous statistical guarantees on uncertainty thresholds.
- **Temperature Scaling**: Restores calibration to overconfident LLM logits.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **Vision Encoders**: Tested on text LLM serving.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: Calibration for model routing.
- **How our inquiry differs**: We apply calibrated logit margins to VLM multiple-choice answers in XLRS-Bench.

---

## 8. Technical Deep-Dive & Architecture Specification

```mermaid
flowchart LR
    A[Visual Input] --> B[Encoder: N/A (Multi-LLM router)]
    B --> C[Projector: N/A]
    C --> D[LLM Backbone: Fast: Llama-3-8B / Heavy: Llama-3-70B]
    D --> E[Predictions: N/A]
```

- **Vision Encoder**: `N/A (Multi-LLM router)`
- **Cross-Modal Projector**: `N/A`
- **Language Backbone**: `Fast: Llama-3-8B / Heavy: Llama-3-70B`
- **Visual Token Budget**: `N/A`

---

## 9. Actionable Takeaways for Our Codebase & Experiments
- [ ] **Calibration Rule**: Apply temperature scaling ($T=1.2$) to Qwen2.5-VL logits before computing margin $M = p(y_1) - p(y_2)$.
- [ ] **Threshold Reliability**: Prevents overconfident wrong predictions from skipping necessary zoom.
