# Machine Extraction: Adaptive Visual Token Sampling via Cross-Modal Attention

- **BibTeX Key**: `zhang2024adaptivetokensampler`
- **Authors**: Hao Zhang, Mengdi Li, Jiayan Teng
- **Venue**: ICLR 2024 (2024)
- **arXiv**: [2402.12870](https://arxiv.org/abs/2402.12870)
- **Code**: https://github.com/THU-Zhang/AdaptiveSampler
- **Category**: 03_token_pruning_and_efficiency
- **Relevance**: 3 / 5 (Moderate Efficiency Prior)

## Abstract
We introduce Adaptive Visual Token Sampling (ATS). ATS formulates token selection as a differentiable subset sampling problem conditioned on the textual question, learning to sample dense tokens around queried entities and sparse tokens elsewhere.

## Key Empirical Findings
1. Differentiable sampling learns task-adaptive token allocation policies.
2. Reduces token count by 50% with zero loss on ScienceQA and VQA-v2.
3. Requires end-to-end training.

## Authors' Stated Conclusions
Learned cross-modal sampling outperforms heuristic token dropping.

## Open Challenges & Future Scope
Extension to training-free test-time execution.

## Architectural Profile
- **Vision**: ViT-L/14
- **Projector**: Adaptive Sampling Projector
- **LLM**: LLaMA-7B
- **Tokens**: Variable (Adaptive)
