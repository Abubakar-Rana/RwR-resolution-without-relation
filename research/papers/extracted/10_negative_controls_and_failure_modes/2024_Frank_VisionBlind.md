# Machine Extraction: Vision Models Are Often Blind to High-Frequency Spatial Structures

- **BibTeX Key**: `frank2024visionblind`
- **Authors**: Anette Frank, Letitia Parcalabescu
- **Venue**: CVPRW 2024 (2024)
- **arXiv**: [2405.08912](https://arxiv.org/abs/2405.08912)
- **Code**: https://github.com/Heidelberg-NLP/VisionBlind
- **Category**: 10_negative_controls_and_failure_modes
- **Relevance**: 3 / 5 (Frequency Analysis Prior)

## Abstract
We analyze the frequency response of Vision Transformers. We discover that self-attention layers act as low-pass filters, progressively attenuating high-frequency spatial gradients and retaining only low-frequency semantic blobs.

## Key Empirical Findings
1. Self-attention layers attenuate high spatial frequencies by over 80% after layer 6.
2. Discards fine object boundaries and sub-pixel lines essential for aerial targets.
3. Explains why deep ViT features blur small vehicles and thin roads.

## Authors' Stated Conclusions
Standard Vision Transformers act as low-pass filters, inherently stripping out high-frequency spatial boundaries.

## Open Challenges & Future Scope
Frequency-preserving transformer layers.

## Architectural Profile
- **Vision**: ViT-B/16 & ViT-L/14 with Fourier Analysis
- **Projector**: N/A
- **LLM**: None
- **Tokens**: Native
