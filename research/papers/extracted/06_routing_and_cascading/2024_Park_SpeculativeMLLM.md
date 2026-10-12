# Machine Extraction: Speculative Decoding for Multimodal Language Models

- **BibTeX Key**: `park2024speculativemllm`
- **Authors**: Junhyuk Park, Sangmin Bae
- **Venue**: EMNLP 2024 (2024)
- **arXiv**: [2404.14890](https://arxiv.org/abs/2404.14890)
- **Code**: https://github.com/KAIST-AILab/SpeculativeMLLM
- **Category**: 06_routing_and_cascading
- **Relevance**: 3 / 5 (Moderate Efficiency Prior)

## Abstract
We explore speculative decoding in vision-language models. Using a 1B MLLM as a draft model and a 7B MLLM as target verifier, SpeculativeMLLM achieves a 2.1x wall-clock inference speedup with zero degradation in benchmark accuracy.

## Key Empirical Findings
1. Draft acceptance rate exceeds 75% on visual question answering.
2. 2.1x wall-clock speedup without modifying output distributions.
3. Requires both draft and target models to share identical tokenizers.

## Authors' Stated Conclusions
Speculative decoding delivers lossless throughput acceleration across multimodal language models.

## Open Challenges & Future Scope
Multi-draft speculative pipelines.

## Architectural Profile
- **Vision**: SigLIP-SO400M
- **Projector**: MLP
- **LLM**: Draft: TinyLLaVA-1B / Target: Qwen2-VL-7B
- **Tokens**: Native
