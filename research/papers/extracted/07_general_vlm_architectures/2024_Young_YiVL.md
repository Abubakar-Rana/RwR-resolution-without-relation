# Machine Extraction: Yi-VL: Large Multimodal Models from 01.AI

- **BibTeX Key**: `young2024yivl`
- **Authors**: Alex Young, Bei Chen, Chao Li, Chengen Huang, Ge Zhang, Guanwei Ding
- **Venue**: arXiv preprint (2024)
- **arXiv**: [2403.04780](https://arxiv.org/abs/2403.04780)
- **Code**: https://github.com/01-ai/Yi
- **Category**: 07_general_vlm_architectures
- **Relevance**: 3 / 5 (Moderate Architectural Prior)

## Abstract
We present Yi-VL, built on the Yi language model family. Yi-VL combines features from two distinct vision encoders to capture complementary semantic and low-level representations, achieving strong multimodal reasoning.

## Key Empirical Findings
1. Concatenating two distinct vision encoders (CLIP + OpenCLIP) enriches visual representations.
2. Scales successfully to 34B language parameters.
3. Higher parameter size improves complex reasoning but does not fix small object blindness.

## Authors' Stated Conclusions
Dual vision encoders provide complementary features, but language parameter scaling alone cannot overcome input resolution limits.

## Open Challenges & Future Scope
Dynamic resolution tiling.

## Architectural Profile
- **Vision**: Dual ViT (ViT-H-14 + ViT-bigG)
- **Projector**: Three-layer MLP
- **LLM**: Yi-34B / Yi-6B
- **Tokens**: 1,024 tokens
