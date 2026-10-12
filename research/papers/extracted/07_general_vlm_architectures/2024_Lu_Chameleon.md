# Machine Extraction: Chameleon: Mixed-Modal Early-Fusion Foundation Models

- **BibTeX Key**: `lu2024chameleon`
- **Authors**: Chameleon Team, Meta AI
- **Venue**: arXiv preprint (2024)
- **arXiv**: [2405.09818](https://arxiv.org/abs/2405.09818)
- **Code**: https://github.com/facebookresearch/chameleon
- **Category**: 07_general_vlm_architectures
- **Relevance**: 4 / 5 (Foundational Early-Fusion Architecture)

## Abstract
We present Chameleon, a family of early-fusion foundation models capable of generating and reasoning over interleaved image-and-text sequences. By quantizing images into discrete tokens and training from scratch, Chameleon achieves seamless mixed-modal generation.

## Key Empirical Findings
1. Discrete image tokenization enables unified autoregressive modeling of text and image generation.
2. Extreme quantization loss on fine image details (1024 discrete tokens cannot represent small aerial objects).
3. Strong on image-text interleaving, but lags behind dual-encoder models on fine-grained perception.

## Authors' Stated Conclusions
Early-fusion discrete tokenization enables unified generation, but incurs high information loss on fine spatial details compared to continuous feature encoders.

## Open Challenges & Future Scope
Continuous early-fusion transformers.

## Architectural Profile
- **Vision**: VQ-VAE Image Tokenizer (1024 discrete tokens)
- **Projector**: Embedding lookup
- **LLM**: Chameleon 7B / 34B Transformer
- **Tokens**: Fixed 1,024 discrete tokens
