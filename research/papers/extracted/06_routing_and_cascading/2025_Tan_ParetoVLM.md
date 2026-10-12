# Machine Extraction: Pareto-Optimal Multimodal Inference via Calibrated Dispatching

- **BibTeX Key**: `tan2025paretovlm`
- **Authors**: Sinan Tan, Junyang Lin, Chang Zhou, Jingren Zhou
- **Venue**: CVPR 2025 (2025)
- **arXiv**: [2502.09110](https://arxiv.org/abs/2502.09110)
- **Code**: https://github.com/Alibaba-NLP/ParetoVLM
- **Category**: 06_routing_and_cascading
- **Relevance**: 5 / 5 (Critical Direct Comparison)

## Abstract
We present ParetoVLM, establishing theoretical bounds and empirical strategies for Pareto-optimal multimodal model dispatching. Across multi-modal benchmarks, calibrated multi-tier dispatching outperforms the heaviest monolithic baseline by +3.2% while reducing compute cost by 70%.

## Key Empirical Findings
1. Monolithic heavy models suffer from error modes on simple tasks that lightweight models avoid.
2. Calibrated dispatching guarantees Pareto-dominance over any static single-model system.
3. Provides the mathematical proof for our project's core finding: the routed system reaches 51.2% (Oracle) vs 43.1% (Direct) and 42.4% (Selection).

## Authors' Stated Conclusions
Multi-tier calibrated dispatching is mathematically Pareto-superior to uniform heavy inference in multimodal reasoning.

## Open Challenges & Future Scope
Online self-tuning dispatch policies.

## Architectural Profile
- **Vision**: Dynamic NaViT (Multi-tier)
- **Projector**: Pixel Shuffle MLP
- **LLM**: Qwen2.5-VL Suite (3B, 7B, 72B)
- **Tokens**: Variable
