# Machine Extraction: Cost-Aware Dynamic Routing in Visual Foundation Models

- **BibTeX Key**: `huang2025costawarerouting`
- **Authors**: Tianhe Ren, Siyuan Huang, Yuhui Shang
- **Venue**: CVPR 2025 (2025)
- **arXiv**: [2501.09840](https://arxiv.org/abs/2501.09840)
- **Code**: https://github.com/THU-Huang/CostAwareRouting
- **Category**: 06_routing_and_cascading
- **Relevance**: 4 / 5 (High Routing Prior)

## Abstract
We formulate vision-language model routing as budget-constrained utility maximization. Given a strict target latency budget (e.g. 500ms or 2,000ms), our router learns the optimal allocation of queries across fast, medium, and heavy multimodal models.

## Key Empirical Findings
1. Constrained optimization produces distinct routing thresholds for different latency ceilings.
2. Under a 3,000ms budget, the optimal policy routes 75% of queries to fast overview and 25% to slow zoom.
3. Achieves 96% of unconstrained accuracy at 30% of total compute cost.

## Authors' Stated Conclusions
Budget-constrained routing provides a principled mathematical framework for real-world VLM deployment.

## Open Challenges & Future Scope
Adaptive online threshold updates.

## Architectural Profile
- **Vision**: Multi-scale ViT
- **Projector**: MLP
- **LLM**: Multi-LLM suite
- **Tokens**: Variable
