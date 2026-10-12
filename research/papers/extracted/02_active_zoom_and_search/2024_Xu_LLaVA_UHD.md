# Machine Extraction: LLaVA-UHD: An LMM Perceiving Any Aspect Ratio and High-Resolution Images

- **BibTeX Key**: `xu2024llavauhd`
- **Authors**: Ronghao Xu, Yuan Yao, Ziqi Wang, Jiayan Teng, Mengdi Li
- **Venue**: arXiv preprint (2024)
- **arXiv**: [2403.11703](https://arxiv.org/abs/2403.11703)
- **Code**: https://github.com/THUNLP-MT/LLaVA-UHD
- **Category**: 02_active_zoom_and_search
- **Relevance**: 4 / 5 (High Architectural Prior)

## Abstract
We present LLaVA-UHD, an efficient multimodal architecture perceiving images of any aspect ratio and high resolution. LLaVA-UHD partitions images into variable-sized slices matching native aspect ratio, compressing each slice into visual tokens via a spatial resampler.

## Key Empirical Findings
1. Dynamic slicing prevents aspect ratio distortion that degrades aerial object shapes.
2. Slices processed in parallel with a shared spatial position schema.
3. Achieves SOTA on OCR and fine visual benchmarks with 94% fewer tokens.

## Authors' Stated Conclusions
Aspect-ratio-preserving slicing is superior to fixed grid resizing.

## Open Challenges & Future Scope
Scaling to gigapixel imagery and handling multi-scale overhead views.

## Architectural Profile
- **Vision**: CLIP ViT-L/14-336
- **Projector**: Spatial Resampler (Compresses to 64 tokens/slice)
- **LLM**: Vicuna-7B
- **Tokens**: Variable (64 tokens per slice)
