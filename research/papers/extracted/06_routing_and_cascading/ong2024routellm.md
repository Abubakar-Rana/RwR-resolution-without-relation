# RouteLLM: Learning to Route LLMs with Preference Data

- **Authors**: Isaac Ong, Amjad Almahairi, Vincent Wu, Wei-Lin Chiang, Tianhao Wu, Joseph E. Gonzalez, Ion Stoica
- **Year**: 2024
- **Venue**: arXiv preprint
- **arXiv**: 2406.18665
- **URL**: https://arxiv.org/abs/2406.18665
- **BibTeX Key**: `ong2024routellm`

## Abstract
Deploying frontier Large Language Models at scale incurs immense serving costs. In many practical applications, however, simpler queries can be resolved by cheaper open-source models, while only difficult queries require expensive frontier models. We present RouteLLM, a framework for learning to route queries between cheap and strong models using human preference data. We evaluate four routing mechanisms: random, similarity-based, matrix factorization, and causal LLM classifiers. Evaluated across major LLM benchmarks (MT-Bench, MMLU, GSM8K), RouteLLM cuts serving costs by over 50% while maintaining 95% of frontier model quality, and improves overall accuracy over any single static model on heterogeneous query distributions.

## Key Extracted Contributions
1. A lightweight matrix factorization or modern BERT classifier can route queries with <5ms latency.
2. Query difficulty varies wildly: over 60% of queries do not benefit from expensive model computation.
3. Routing outperforms either model alone when models exhibit complementary strengths on different query types.
