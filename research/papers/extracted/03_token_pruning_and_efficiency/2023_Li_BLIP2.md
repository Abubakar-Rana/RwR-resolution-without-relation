# Machine Extraction: BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models

- **BibTeX Key**: `li2023blip2`
- **Authors**: Junnan Li, Dongxu Li, Silvio Savarese, Steven Hoi
- **Venue**: ICML 2023 (2023)
- **arXiv**: [2301.12597](https://arxiv.org/abs/2301.12597)
- **Code**: https://github.com/salesforce/LAVIS
- **Category**: 03_token_pruning_and_efficiency
- **Relevance**: 4 / 5 (Foundational Q-Former Prior)

## Abstract
We propose BLIP-2, a compute-efficient pre-training strategy bootstrapping from off-the-shelf frozen vision encoders and frozen LLMs via a lightweight Querying Transformer (Q-Former). BLIP-2 achieves SOTA zero-shot performance with significantly fewer trainable parameters.

## Key Empirical Findings
1. Q-Former bridges modality gaps without fine-tuning heavy vision or language backbones.
2. Extracts 32 visual tokens from 257 image tokens.
3. Acts as an information bottleneck that suppresses high-frequency spatial noise.

## Authors' Stated Conclusions
Two-stage connector pre-training effectively aligns visual features to frozen LLM representations.

## Open Challenges & Future Scope
Handling high-resolution multi-scale inputs.

## Architectural Profile
- **Vision**: ViT-L/14 & EVA-CLIP
- **Projector**: Q-Former (32 queries)
- **LLM**: OPT-6.7B / Flan-T5-XXL
- **Tokens**: Fixed 32 tokens
