# Machine Extraction: Context-Preserving Zoom for Dense Aerial Object Understanding

- **BibTeX Key**: `zheng2025contextzoom`
- **Authors**: Kai Zheng, Haoliang Wang, Wen Yang
- **Venue**: CVPR 2025 (2025)
- **arXiv**: [2502.11209](https://arxiv.org/abs/2502.11209)
- **Code**: https://github.com/WHU-USI/ContextZoom
- **Category**: 02_active_zoom_and_search
- **Relevance**: 5 / 5 (Critical Direct Baseline)

## Abstract
Active zooming in aerial imagery typically isolates crops, severing geographical context. ContextZoom introduces a dual-stream architecture where high-resolution crop features continuously cross-attend to the low-resolution global overview before entering the LLM.

## Key Empirical Findings
1. Preserves global cardinal orientation while zooming into fine targets.
2. Closes 75% of the relational accuracy drop observed in standard tile selection.
3. Increases latency by only 12% over single-stream zoom.

## Authors' Stated Conclusions
Continuous cross-scale feature binding mitigates the relational reasoning penalty of zoom.

## Open Challenges & Future Scope
Integrating dynamic routing to bypass zooming on non-perception queries.

## Architectural Profile
- **Vision**: SigLIP-SO400M (Global + Local)
- **Projector**: Cross-Scale Attention Resampler
- **LLM**: Qwen2-VL-7B
- **Tokens**: 1,536 tokens
