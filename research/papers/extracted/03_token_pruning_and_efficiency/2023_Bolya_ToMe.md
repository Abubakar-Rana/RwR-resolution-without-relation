# Machine Extraction: Token Merging: Your ViT But Faster

- **BibTeX Key**: `bolya2023tome`
- **Authors**: Daniel Bolya, Cheng-Yang Fu, Xiaoliang Dai, Peizhao Zhang, Christoph Feichtenhofer, Judy Hoffman
- **Venue**: ICLR 2023 (2023)
- **arXiv**: [2210.09461](https://arxiv.org/abs/2210.09461)
- **Code**: https://github.com/facebookresearch/ToMe
- **Category**: 03_token_pruning_and_efficiency
- **Relevance**: 4 / 5 (Foundational Pruning Prior)

## Abstract
We present Token Merging (ToMe), a simple, training-free method to accelerate Vision Transformers. ToMe uses bipartite soft matching to merge redundant tokens progressively between self-attention layers, reducing token count while maintaining representation capacity.

## Key Empirical Findings
1. Merging redundant tokens is superior to dropping them because merged tokens retain accumulated information.
2. Accelerates ViT forward pass by 2x with negligible loss in accuracy.
3. Completely training-free.

## Authors' Stated Conclusions
Bipartite token merging preserves information fidelity better than hard token pruning.

## Open Challenges & Future Scope
Cross-modal token merging in vision-language models.

## Architectural Profile
- **Vision**: ViT-B/16 & ViT-L/16 with ToMe
- **Projector**: N/A
- **LLM**: None
- **Tokens**: Merged dynamically per layer
