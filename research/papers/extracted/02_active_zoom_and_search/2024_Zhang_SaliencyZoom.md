# Machine Extraction: Saliency-Guided Adaptive Zoom for Ultra-High Resolution Vision

- **BibTeX Key**: `zhang2024saliencyzoom`
- **Authors**: Yuan Zhang, Lin Chen, Haoran Wei, Xiangyu Zhang
- **Venue**: CVPR 2024 (2024)
- **arXiv**: [2404.09210](https://arxiv.org/abs/2404.09210)
- **Code**: https://github.com/Megvii-BaseDetection/SaliencyZoom
- **Category**: 02_active_zoom_and_search
- **Relevance**: 4 / 5 (High Algorithmic Relevance)

## Abstract
We propose SaliencyZoom, a fast two-stage pipeline for ultra-high-resolution images. A lightweight convolutional saliency head scans the downsampled image in <5ms, identifying top-k salient patches for high-resolution evaluation.

## Key Empirical Findings
1. Saliency scanning runs in 4.2ms, adding negligible overhead.
2. Captures 94% of small target objects across benchmark datasets.
3. Pure visual saliency misses semantic targets specified by text queries if the targets are low-contrast.

## Authors' Stated Conclusions
Saliency provides fast candidate generation but must be paired with semantic text guidance.

## Open Challenges & Future Scope
Text-conditioned saliency filtering.

## Architectural Profile
- **Vision**: MobileNet-V3 (Saliency) + ViT-L (Zoom)
- **Projector**: Linear
- **LLM**: None (Detection focus)
- **Tokens**: Variable
