# Machine Extraction: LM-Nav: Robotic Navigation with Large Language Models

- **BibTeX Key**: `shah2024lmnav`
- **Authors**: Dhruv Shah, Blazej Osinski, Brian Ichter, Sergey Levine
- **Venue**: CoRL 2023 (2023)
- **arXiv**: [2207.04429](https://arxiv.org/abs/2207.04429)
- **Code**: https://sites.google.com/view/lmnav
- **Category**: 09_embodied_and_3d_spatial_priors
- **Relevance**: 4 / 5 (High Navigation Prior)

## Abstract
We present LM-Nav, enabling long-horizon robotic navigation from natural language instructions without any paired language-navigation training data. LM-Nav decomposes navigation into language parsing (GPT-3), visual landmark retrieval (CLIP), and graph planning over a topological map (ViNG).

## Key Empirical Findings
1. Three-way modular separation (language parser + visual retriever + topological graph planner) outperforms monolithic end-to-end models.
2. Topological visual graph handles long-horizon navigation with zero spatial hallucination.
3. Entire system is training-free.

## Authors' Stated Conclusions
Decoupling visual perception, linguistic planning, and topological graph search provides reliable long-horizon spatial execution.

## Open Challenges & Future Scope
Dynamic topological map expansion.

## Architectural Profile
- **Vision**: CLIP ViT-B/32 + ViNG Topological Graph
- **Projector**: Topological Graph Search
- **LLM**: GPT-3 (text-davinci-002)
- **Tokens**: N/A (API calls)
