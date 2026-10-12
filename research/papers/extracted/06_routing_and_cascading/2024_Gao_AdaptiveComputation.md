# Machine Extraction: Adaptive Early Exiting in Multimodal Transformers

- **BibTeX Key**: `gao2024adaptivecomputation`
- **Authors**: Jianfei Gao, Hao Yuan, Siyuan Li
- **Venue**: ECCV 2024 (2024)
- **arXiv**: [2407.14201](https://arxiv.org/abs/2407.14201)
- **Code**: https://github.com/GaoJianfei/AdaptiveExit
- **Category**: 06_routing_and_cascading
- **Relevance**: 3 / 5 (Moderate Efficiency Prior)

## Abstract
We propose Adaptive Early Exiting for MLLMs. By attaching intermediate classification heads at transformer layers 8, 16, and 24, our model evaluates prediction confidence dynamically, exiting early on simple queries and saving 45% compute.

## Key Empirical Findings
1. Over 40% of queries can exit by layer 16 with zero accuracy loss.
2. Complex relational and reasoning queries require deep layers.
3. Calibrated entropy thresholds prevent premature exits on difficult items.

## Authors' Stated Conclusions
Depth of transformer reasoning varies dramatically across question types; early exiting captures this heterogeneity.

## Open Challenges & Future Scope
Adaptive visual token depth.

## Architectural Profile
- **Vision**: CLIP ViT-L/14
- **Projector**: MLP
- **LLM**: LLaMA-7B with Early Exit Heads
- **Tokens**: 576 tokens
