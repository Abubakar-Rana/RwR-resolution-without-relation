# FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance

- **Authors**: Lingjiao Chen, Matei Zaharia, James Zou
- **Year**: 2023
- **Venue**: NeurIPS 2023
- **arXiv**: 2305.05176
- **URL**: https://arxiv.org/abs/2305.05176
- **BibTeX Key**: `chen2023frugalgpt`

## Abstract
Commercial Large Language Model (LLM) APIs vary widely in cost, latency, and capability. We present FrugalGPT, a flexible framework that leverages cascades of LLMs to reduce costs while improving accuracy. FrugalGPT introduces an LLM cascade strategy that adaptively queries a sequence of models, evaluating response quality using learned scoring functions and escalating only when necessary. On representative natural language benchmarks, FrugalGPT reduces operational inference costs by up to 98% while matching the performance of the best commercial LLM, or improves performance over any individual model by 4% at equal cost.

## Key Extracted Contributions
1. Cascading models sequentially achieves a strictly superior Pareto frontier than using any single model statically.
2. A learned scoring function can reliably predict whether a cheaper model's response is correct.
3. The optimal cascade order places the cheapest high-precision model first.
