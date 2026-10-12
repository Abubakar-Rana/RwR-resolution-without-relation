# Machine Extraction: When and Why Vision-Language Models Behave Like Bags-of-Words

- **BibTeX Key**: `yuksekgonul2024aro`
- **Authors**: Mert Yuksekgonul, Federico Bianchi, Pratyush Kalluri, Dan Jurafsky, James Zou
- **Venue**: ICLR 2023 (2023)
- **arXiv**: [2210.01936](https://arxiv.org/abs/2210.01936)
- **Code**: https://github.com/mertyg/aro
- **Category**: 10_negative_controls_and_failure_modes
- **Relevance**: 5 / 5 (Foundational Negative Analysis)

## Abstract
We present ARO, benchmarking vision-language models on compositionality. Across multiple model families, we show that contrastive models behave like bag-of-words models: shuffling word order or swapping relational predicates has virtually no effect on retrieval scores.

## Key Empirical Findings
1. Shuffling text caption words reduces retrieval score by less than 5% in standard CLIP.
2. Models cannot distinguish 'the dog is to the left of the cat' from 'the cat is to the left of the dog'.
3. Pretraining on noisy web captions teaches models to correlate co-occurring keywords rather than syntax.

## Authors' Stated Conclusions
Contrastive vision-language pretraining actively penalizes syntactic sensitivity, producing bag-of-words representations.

## Open Challenges & Future Scope
Structure-aware contrastive losses.

## Architectural Profile
- **Vision**: CLIP ViT-B/32 & ViT-L/14
- **Projector**: Linear
- **LLM**: Transformer text encoder
- **Tokens**: Global pooled embedding
