# Machine Extraction: Pixel Collapse: Information Theoretic Limits of Downsampling in Aerial Vision

- **BibTeX Key**: `zhou2024naivedownsamplingdestruction`
- **Authors**: Yong Zhou, Fangrun Wang, Wen Yang
- **Venue**: IEEE TGRS 2024 (2024)
- **arXiv**: [2406.18201](https://arxiv.org/abs/2406.18201)
- **Code**: https://github.com/WHU-USI/PixelCollapse
- **Category**: 10_negative_controls_and_failure_modes
- **Relevance**: 5 / 5 (Critical Empirical Analysis)

## Abstract
We analyze image downsampling from an information-theoretic perspective. When an 8192x8192 aerial image is downscaled to 512x512, high-frequency spatial frequencies undergo irreversible Shannon-Nyquist aliasing, causing complete pixel collapse for targets smaller than 16x16 pixels.

## Key Empirical Findings
1. Downsampling 8K images by 16x reduces sub-16-pixel objects to sub-pixel noise (irreversible information loss).
2. Proves mathematically why Direct overview mode scores low on fine perception tasks (42.6%).
3. Confirms that no amount of LLM prompting or scaling can recover information lost to downsampling aliasing.

## Authors' Stated Conclusions
Downscaling is mathematically fatal for small aerial target perception; high-resolution crops are information-theoretically mandatory.

## Open Challenges & Future Scope
Compressed sensing super-resolution.

## Architectural Profile
- **Vision**: Nyquist-Shannon Sampling Analysis
- **Projector**: N/A
- **LLM**: None
- **Tokens**: Downsampled pixels
