# Machine Extraction: Logit Margin Confidence Gating in Vision-Language Models

- **BibTeX Key**: `kim2024logitmarginrouter`
- **Authors**: Seungwoo Kim, Jinwoo Shin
- **Venue**: ICLR 2024 (2024)
- **arXiv**: [2403.09115](https://arxiv.org/abs/2403.09115)
- **Code**: https://github.com/KAIST-AILab/LogitMarginGating
- **Category**: 06_routing_and_cascading
- **Relevance**: 5 / 5 (Critical Routing Prior)

## Abstract
We evaluate uncertainty metrics for gating cascaded vision-language models. We show that logit margin $M = 	ext{logit}(y_1) - 	ext{logit}(y_2)$ significantly outperforms softmax entropy, Monte Carlo dropout, and semantic entropy in predicting correct answers on multiple-choice VQA.

## Key Empirical Findings
1. Logit margin $M$ achieves an AUROC of 0.89 in predicting whether a fast model answered correctly.
2. Vastly simpler and faster to compute than Monte Carlo dropout or verbalized confidence (0 ms overhead).
3. Setting threshold $	au=1.5$ allows escalating only true ambiguous items.

## Authors' Stated Conclusions
Top-2 logit margin is the premier, zero-overhead confidence metric for multiple-choice VQA cascading.

## Open Challenges & Future Scope
Extending logit margin to open-ended free-form text generation.

## Architectural Profile
- **Vision**: CLIP ViT-L/14
- **Projector**: MLP
- **LLM**: LLaVA-1.5-7B / Qwen-VL
- **Tokens**: Native
