# Machine Extraction: Confidence-Calibrated Routing for Cost-Efficient Multi-LLM Serving

- **BibTeX Key**: `liu2024confidencecalibration`
- **Authors**: Zhuang Liu, Shengbang Tong, Yi Ma
- **Venue**: ICML 2024 (2024)
- **arXiv**: [2405.02110](https://arxiv.org/abs/2405.02110)
- **Code**: https://github.com/CalibratedRouting/CalibratedRoute
- **Category**: 06_routing_and_cascading
- **Relevance**: 4 / 5 (High Routing Prior)

## Abstract
Uncalibrated language model logits lead to poor routing decisions in multi-model serving. We introduce Confidence-Calibrated Routing, applying conformal prediction to establish rigorous confidence guarantees before deciding whether to accept a fast model's output or escalate to a heavy model.

## Key Empirical Findings
1. Raw softmax probabilities are systematically overconfident in modern LLMs.
2. Temperature scaling and conformal calibration restore predictive calibration.
3. Calibrated routing reduces misclassification by 34% compared to raw argmax gating.

## Authors' Stated Conclusions
Probability calibration is mandatory for robust threshold-based escalation in cascaded model serving.

## Open Challenges & Future Scope
Multimodal calibrated routing.

## Architectural Profile
- **Vision**: N/A (Multi-LLM router)
- **Projector**: N/A
- **LLM**: Fast: Llama-3-8B / Heavy: Llama-3-70B
- **Tokens**: N/A
