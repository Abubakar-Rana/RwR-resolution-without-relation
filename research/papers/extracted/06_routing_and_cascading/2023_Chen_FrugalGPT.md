# Machine Extraction: FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Accuracy

- **BibTeX Key**: `chen2023frugalgpt`
- **Authors**: Lingjiao Chen, Matei Zaharia, James Zou
- **Venue**: NeurIPS 2023 (2023)
- **arXiv**: [2305.05176](https://arxiv.org/abs/2305.05176)
- **Code**: https://github.com/stanford-futuredata/FrugalGPT
- **Category**: 06_routing_and_cascading
- **Relevance**: 4 / 5 (Foundational Cascade Prior)

## Abstract
The cost of querying commercial LLMs scales rapidly. We propose FrugalGPT, a cascade framework that learns which combination of LLMs to query for different queries. By routing queries through a progression of LLMs and evaluating scoring functions, FrugalGPT matches GPT-4 accuracy with up to 98% cost savings.

## Key Empirical Findings
1. Cascading queries sequentially from cheap to expensive models outperforms any single model.
2. Simple scoring functions (e.g. logit margin, response length, entropy) effectively predict model success.
3. Counter-intuitively improves accuracy by avoiding large model failure modes on simple queries.

## Authors' Stated Conclusions
Model cascading is fundamentally Pareto-superior to monolithic single-model invocation.

## Open Challenges & Future Scope
Multimodal cascading.

## Architectural Profile
- **Vision**: N/A (Text cascade)
- **Projector**: N/A
- **LLM**: GPT-3 -> Claude-Instant -> GPT-4
- **Tokens**: N/A
