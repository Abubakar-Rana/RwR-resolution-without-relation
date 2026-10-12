# Machine Extraction: Seeing Stone: Measuring Relational Misalignment in Multi-Modal Models

- **BibTeX Key**: `parcalabescu2024seeingstone`
- **Authors**: Letitia Parcalabescu, Michele Cafagna, Lilitta Muradjan, Anette Frank, Iacer Calixto, Albert Gatt
- **Venue**: EMNLP 2022 (2022)
- **arXiv**: [2112.05147](https://arxiv.org/abs/2112.05147)
- **Code**: https://github.com/Letitia-P/aro
- **Category**: 10_negative_controls_and_failure_modes
- **Relevance**: 4 / 5 (Diagnostic Failure Analysis)

## Abstract
We evaluate relational spatial understanding in 20 multimodal models. We show that models exhibit severe relational misalignment: while they recognize the entities involved, they fail to verify spatial relations above random chance.

## Key Empirical Findings
1. Models score 52.3% on binary spatial relation verification (random chance is 50.0%).
2. Left/right and front/behind relations are completely unaligned in visual token space.
3. Object recognition accuracy does not correlate with relational accuracy.

## Authors' Stated Conclusions
Object recognition capability is completely decoupled from spatial relational reasoning capability.

## Open Challenges & Future Scope
Spatially grounded pretraining.

## Architectural Profile
- **Vision**: CLIP, FLAVA, ViLT, ALBEF
- **Projector**: Native
- **LLM**: None (Pre-LLM era)
- **Tokens**: Native
