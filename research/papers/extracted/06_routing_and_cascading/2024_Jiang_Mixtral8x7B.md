# Machine Extraction: Mixtral of Experts

- **BibTeX Key**: `jiang2024mixtral8x7b`
- **Authors**: Albert Q. Jiang, Alexandre Sablayrolles, Antoine Roux, Arthur Mensch, Blanche Savary, Chris Bamford, Devendra Singh Chaplot, Diego de las Casas, Emma Bou Hanna, Florian Bressand, Gianna Lengyel, Guillaume Bour, Guillaume Lample, Lelio Renard Lavaud, Lucile Saulnier, Marie-Anne Lachaux, Pierre Stock, Sandeep Subramanian, Sophia Yang, Szymon Antoniak, Teven Le Scao, Theophile Gervet, Thibaut Lavril, Thomas Wang, Timothee Lacroix, William El Sayed
- **Venue**: arXiv preprint (2024)
- **arXiv**: [2401.04088](https://arxiv.org/abs/2401.04088)
- **Code**: https://github.com/mistralai/mistral-src
- **Category**: 06_routing_and_cascading
- **Relevance**: 4 / 5 (Foundational MoE Architecture)

## Abstract
We present Mixtral 8x7B, a Sparse Mixture of Experts (SMoE) language model. Mixtral has 46.7B total parameters but uses only 12.9B parameters per token during inference, outperforming Llama 2 70B on most benchmarks with 6x faster inference.

## Key Empirical Findings
1. Sparse routing activates only 25% of total parameters per token without quality degradation.
2. Routing weights dynamically adapt across mathematical, spatial, and linguistic domains.
3. Proves the computational superiority of sparse conditional execution over monolithic dense models.

## Authors' Stated Conclusions
Sparse conditional computation is the premier architecture for scaling capacity within strict latency budgets.

## Open Challenges & Future Scope
Multimodal sparse MoE backbones.

## Architectural Profile
- **Vision**: None
- **Projector**: N/A
- **LLM**: Mixtral 8x7B (SMoE)
- **Tokens**: N/A
