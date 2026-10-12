# Machine Extraction: LLaVA-NeXT: Improved Reasoning, OCR, and World Knowledge

- **BibTeX Key**: `liu2024llavanext`
- **Authors**: Haotian Liu, Chunyuan Li, Yuheng Li, Bo Li, Yuanhan Zhang, Sheng Shen, Yong Jae Lee
- **Venue**: Blogpost / arXiv preprint (2024)
- **arXiv**: [2405.01432](https://arxiv.org/abs/2405.01432)
- **Code**: https://github.com/haotian-liu/LLaVA
- **Category**: 02_active_zoom_and_search
- **Relevance**: 4 / 5 (High Industry Standard)

## Abstract
LLaVA-NeXT extends open-source LMM performance by scaling resolution up to 4x more pixels using AnyRes dynamic grids. By appending an overview thumbnail token sequence to the tiled high-resolution patches, LLaVA-NeXT significantly improves OCR and detailed reasoning.

## Key Empirical Findings
1. Appending the overview thumbnail is critical; removing it causes severe spatial degradation.
2. Dynamic grid selection adapts to natural aspect ratios.
3. Standard AnyRes grids still top out at ~2K resolution; cannot ingest 8K imagery directly.

## Authors' Stated Conclusions
Multi-crop architectures must always include a global thumbnail to anchor spatial context.

## Open Challenges & Future Scope
Scaling beyond 4 crops to gigapixel hierarchies.

## Architectural Profile
- **Vision**: CLIP ViT-L/14-336 with AnyRes
- **Projector**: Two-layer MLP
- **LLM**: Vicuna-7B / Llama-3-8B / Qwen-1.5-72B
- **Tokens**: 2,880 tokens (5 crops x 576 tokens)
