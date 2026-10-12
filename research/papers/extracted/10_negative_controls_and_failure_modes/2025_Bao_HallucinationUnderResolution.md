# Machine Extraction: Resolution-Induced Hallucination in Multi-Crop Vision Language Architectures

- **BibTeX Key**: `bao2025hallucinationunderresolution`
- **Authors**: Yushi Bao, Zhilin Yang, Guohao Li
- **Venue**: CVPR 2025 (2025)
- **arXiv**: [2501.12980](https://arxiv.org/abs/2501.12980)
- **Code**: https://github.com/THU-Bao/ResolutionHallucination
- **Category**: 10_negative_controls_and_failure_modes
- **Relevance**: 4 / 5 (High Failure Analysis)

## Abstract
We explore resolution-induced hallucination in multi-crop MLLMs. When models are presented with high-resolution crops of uninformative background, they exhibit strong conversational bias to find objects that do not exist, increasing hallucination rates by 38%.

## Key Empirical Findings
1. Providing empty crops increases false positive object hallucinations by 38%.
2. Conversational pragmatics bias: models assume provided crops must contain relevant targets.
3. Confirms that selecting empty or low-relevance tiles actively harms model accuracy.

## Authors' Stated Conclusions
Selecting false-positive background tiles actively induces conversational hallucination in MLLMs.

## Open Challenges & Future Scope
Explicit 'empty tile' tokens in training.

## Architectural Profile
- **Vision**: CLIP ViT-L/14 with Multi-Crop
- **Projector**: MLP
- **LLM**: Vicuna-7B / Llama-3-8B
- **Tokens**: Multi-crop sequences
