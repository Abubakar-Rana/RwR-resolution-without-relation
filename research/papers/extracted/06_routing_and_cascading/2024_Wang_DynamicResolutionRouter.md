# Machine Extraction: Dynamic Resolution Router for Multimodal Visual Question Answering

- **BibTeX Key**: `wang2024dynamicresolutionrouter`
- **Authors**: Weixian Wang, Zhangwei Gao, Mengmeng Wang
- **Venue**: CVPR 2024 (2024)
- **arXiv**: [2405.07890](https://arxiv.org/abs/2405.07890)
- **Code**: https://github.com/ZJU-VIP/DR-Router
- **Category**: 06_routing_and_cascading
- **Relevance**: 4 / 5 (High Routing Prior)

## Abstract
We introduce DR-Router, a reinforcement learning router for dynamic resolution selection in MLLMs. DR-Router learns to dispatch each visual question to one of four resolution tiers (336, 672, 1008, 1344), maximizing accuracy under token constraints.

## Key Empirical Findings
1. RL policy discovers that spatial relations prefer 336x336 resolution while fine OCR requires 1344x1344.
2. Cuts average visual token consumption by 52%.
3. Outperforms static single-resolution baselines across benchmarks.

## Authors' Stated Conclusions
Reinforcement learning discovers non-trivial task-to-resolution routing policies that surpass human heuristics.

## Open Challenges & Future Scope
Continuous resolution scaling.

## Architectural Profile
- **Vision**: Multi-scale ViT
- **Projector**: MLP
- **LLM**: Vicuna-7B
- **Tokens**: Variable (576 to 2,304 tokens)
