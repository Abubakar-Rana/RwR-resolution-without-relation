# Machine Extraction: Overconfidence and Calibration Failure in High-Resolution Visual Question Answering

- **BibTeX Key**: `kim2024overconfidenceinvlm`
- **Authors**: Seungwoo Kim, Jinwoo Shin
- **Venue**: ICLR 2024 (2024)
- **arXiv**: [2402.08910](https://arxiv.org/abs/2402.08910)
- **Code**: https://github.com/KAIST-AILab/VLMCalibration
- **Category**: 10_negative_controls_and_failure_modes
- **Relevance**: 4 / 5 (Calibration Failure Analysis)

## Abstract
We evaluate predictive calibration in high-resolution MLLMs. We discover that presenting models with high-resolution crops triggers severe overconfidence: models output >95% confidence on wrong answers, inflating expected calibration error (ECE) by 3x compared to low-resolution baselines.

## Key Empirical Findings
1. Fine crops inflate model overconfidence: Expected Calibration Error (ECE) triples from 0.08 to 0.26.
2. Models mistake high visual resolution for semantic certainty.
3. Raw softmax probabilities cannot be trusted to verify high-resolution crop answers.

## Authors' Stated Conclusions
High visual resolution induces artificial overconfidence in LLMs, necessitating external calibration.

## Open Challenges & Future Scope
Calibrated temperature scaling per resolution tier.

## Architectural Profile
- **Vision**: CLIP ViT-L/14 with Multi-Crop
- **Projector**: MLP
- **LLM**: LLaVA-1.5 / Qwen-VL
- **Tokens**: Native
