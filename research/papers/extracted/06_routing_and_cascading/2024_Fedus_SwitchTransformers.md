# Machine Extraction: Switch Transformers: Scaling to Trillion Parameter Models with Simple Routing

- **BibTeX Key**: `fedus2024switchtransformers`
- **Authors**: William Fedus, Barret Zoph, Noam Shazeer
- **Venue**: JMLR 2022 (2022)
- **arXiv**: [2101.03961](https://arxiv.org/abs/2101.03961)
- **Code**: https://github.com/google-research/t5x
- **Category**: 06_routing_and_cascading
- **Relevance**: 4 / 5 (Foundational MoE Literature)

## Abstract
We introduce Switch Transformers, scaling parameter count up to trillion parameters while preserving computational cost per token. By routing each token to a single expert (top-1 routing), Switch Transformers simplifies routing and maximizes throughput.

## Key Empirical Findings
1. Top-1 routing is simpler, faster, and competitive with top-2 gating.
2. Drastically reduces inter-device communication overhead.
3. Scales model parameters by 7x at constant compute budget.

## Authors' Stated Conclusions
Hard top-1 routing provides the highest hardware efficiency and lowest dispatch latency.

## Open Challenges & Future Scope
Dynamic capacity factors per expert.

## Architectural Profile
- **Vision**: None
- **Projector**: N/A
- **LLM**: Switch-T5 (up to 1.6T parameters)
- **Tokens**: N/A
