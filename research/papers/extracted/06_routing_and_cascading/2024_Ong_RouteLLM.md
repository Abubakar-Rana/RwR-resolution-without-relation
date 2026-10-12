# Machine Extraction: RouteLLM: Learning to Route to Large Language Models with Preference Data

- **BibTeX Key**: `ong2024routellm`
- **Authors**: Isaac Ong, Amjad Almahairi, Vincent Wu, Wei-Lin Chiang, Tianhao Wu, Joseph E. Gonzalez, Mosharaf Chowdhury, Ion Stoica
- **Venue**: arXiv preprint (2024)
- **arXiv**: [2406.18665](https://arxiv.org/abs/2406.18665)
- **Code**: https://github.com/lm-sys/RouteLLM
- **Category**: 06_routing_and_cascading
- **Relevance**: 5 / 5 (Critical Routing Prior)

## Abstract
Deploying state-of-the-art LLMs is cost-prohibitive. We introduce RouteLLM, training lightweight routers on preference data to dynamically dispatch user queries to a small, fast model or a large, capable model. RouteLLM achieves up to 85% cost reduction while maintaining 95% SOTA benchmark performance.

## Key Empirical Findings
1. Lightweight routers (ModernBERT or matrix factorization) route queries effectively with <5ms overhead.
2. Dispatches easy and specialized queries to cheap models while saving expensive models for complex reasoning.
3. Establishes Pareto-optimal frontiers between inference cost/latency and task accuracy.

## Authors' Stated Conclusions
Dynamic routing across heterogeneous model pathways achieves superior Pareto efficiency compared to any individual model.

## Open Challenges & Future Scope
Multimodal routing across visual resolutions and tool-use pipelines.

## Architectural Profile
- **Vision**: N/A (Text router)
- **Projector**: N/A
- **LLM**: Router: ModernBERT / Target: GPT-4 & Mixtral
- **Tokens**: N/A
