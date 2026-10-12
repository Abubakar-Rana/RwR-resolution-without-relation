# Machine Extraction: Perceiver-Based Cross-Attention for Efficient Multimodal Aggregation

- **BibTeX Key**: `zhao2024perceivercross`
- **Authors**: Liang Zhao, Pengfei Chen, Bo Du
- **Venue**: IEEE TGRS 2024 (2024)
- **arXiv**: [2404.14810](https://arxiv.org/abs/2404.14810)
- **Code**: https://github.com/WHU-Geo/PerceiverCross
- **Category**: 03_token_pruning_and_efficiency
- **Relevance**: 3 / 5 (Moderate Prior)

## Abstract
We explore Perceiver cross-attention for multimodal remote sensing aggregation. Learnable latent queries compress multi-temporal and high-resolution features into a compact representation for conversational reasoning.

## Key Empirical Findings
1. Perceiver resamplers compress multi-temporal images into fixed 256 tokens.
2. Preserves temporal change signals while filtering stationary background.
3. Lacks precise pixel coordinate grounding for small targets.

## Authors' Stated Conclusions
Perceiver cross-attention excels at global semantic summarization but blurs exact object coordinates.

## Open Challenges & Future Scope
Coordinate-guided latent queries.

## Architectural Profile
- **Vision**: ViT-L/14
- **Projector**: Perceiver Resampler (256 queries)
- **LLM**: Vicuna-7B
- **Tokens**: 256 tokens
