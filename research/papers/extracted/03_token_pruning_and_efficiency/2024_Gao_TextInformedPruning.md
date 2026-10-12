# Machine Extraction: Text-Informed Token Selection for Efficient Vision-Language Models

- **BibTeX Key**: `gao2024textinformedpruning`
- **Authors**: Zhangwei Gao, Weixian Wang, Mengmeng Wang
- **Venue**: CVPR 2024 (2024)
- **arXiv**: [2406.01230](https://arxiv.org/abs/2406.01230)
- **Code**: https://github.com/ZJU-VIP/TextPruning
- **Category**: 03_token_pruning_and_efficiency
- **Relevance**: 3 / 5 (Moderate Efficiency Prior)

## Abstract
We present Text-Informed Token Selection (TITS), an early pruning technique for vision-language models. By evaluating cross-attention between visual tokens and textual question tokens at layer 1, TITS filters out irrelevant visual tokens, speeding up inference by 1.8x.

## Key Empirical Findings
1. Layer-1 cross-attention provides a reliable signal for discarding irrelevant background.
2. Speeds up LLM prefill phase by 45%.
3. Preserves object grounding tokens.

## Authors' Stated Conclusions
Early cross-attention signal is sufficient to identify task-irrelevant visual regions.

## Open Challenges & Future Scope
Adaptive pruning thresholds per layer.

## Architectural Profile
- **Vision**: CLIP ViT-L/14
- **Projector**: Linear
- **LLM**: Vicuna-7B
- **Tokens**: Pruned by 40%
