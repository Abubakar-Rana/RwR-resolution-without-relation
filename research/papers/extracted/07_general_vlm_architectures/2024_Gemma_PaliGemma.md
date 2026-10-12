# Machine Extraction: PaliGemma: A Versatile 3B VLM for Transfer

- **BibTeX Key**: `gemma2024paligemma`
- **Authors**: Lucas Beyer, Andreas Steiner, Andre Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, Thomas Kipf, Juraj Gotkowski, Ali Elqursh, Mostafa Dehghani, et al.
- **Venue**: arXiv preprint (2024)
- **arXiv**: [2407.07726](https://arxiv.org/abs/2407.07726)
- **Code**: https://github.com/google-research/big_vision
- **Category**: 07_general_vlm_architectures
- **Relevance**: 4 / 5 (High Lightweight Baseline)

## Abstract
We present PaliGemma, a versatile 3B vision-language model trained for fine-tuning transfer. PaliGemma connects a SigLIP-SO400M vision encoder to a Gemma-2B language model, achieving state-of-the-art transfer results across diverse vision benchmarks.

## Key Empirical Findings
1. Compact 3B parameter size runs in <100ms per image on modern GPUs.
2. Strong visual grounding performance when fine-tuned with coordinate tokens.
3. Native resolution support up to 896x896.

## Authors' Stated Conclusions
Lightweight 3B models achieve competitive grounding performance when initialized with strong vision encoders (SigLIP).

## Open Challenges & Future Scope
PaliGemma-2 scaling.

## Architectural Profile
- **Vision**: SigLIP-SO400M-448
- **Projector**: Linear Projection
- **LLM**: Gemma-2B
- **Tokens**: 256 or 1,024 tokens
