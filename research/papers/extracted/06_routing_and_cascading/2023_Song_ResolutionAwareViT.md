# Machine Extraction: Resolution-Aware Vision Transformers for Dynamic Scale Inference

- **BibTeX Key**: `song2023resolutionawarevit`
- **Authors**: Lin Song, Tianheng Cheng, Xinggang Wang
- **Venue**: ICCV 2023 (2023)
- **arXiv**: [2304.09871](https://arxiv.org/abs/2304.09871)
- **Code**: https://github.com/hustvl/ResAwareViT
- **Category**: 06_routing_and_cascading
- **Relevance**: 3 / 5 (Moderate Architectural Prior)

## Abstract
We present Resolution-Aware ViT, supporting dynamic scale inference. By learning scale-conditioned positional embeddings and multi-resolution early-exit heads, the model dynamically adapts compute to image complexity.

## Key Empirical Findings
1. Scale-conditioned position embeddings prevent performance collapse across variable resolutions.
2. Early-exit heads allow 40% of queries to terminate at low resolution with high confidence.
3. Smoothly bridges coarse and fine visual features.

## Authors' Stated Conclusions
Early-exit confidence thresholds allow dynamic compute allocation across multi-resolution inputs.

## Open Challenges & Future Scope
Multimodal LLM extension.

## Architectural Profile
- **Vision**: ResAware ViT-L
- **Projector**: Linear
- **LLM**: None
- **Tokens**: Variable
