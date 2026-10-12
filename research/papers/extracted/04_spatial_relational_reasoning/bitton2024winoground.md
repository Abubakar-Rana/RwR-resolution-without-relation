# Beyond Winoground: Probing Spatial Prepositions and Compositionality in VLMs

- **Authors**: Yonatan Bitton, Gabriel Stanovsky, Roy Schwartz
- **Year**: 2024
- **Venue**: EMNLP 2024
- **arXiv**: 2405.11234
- **URL**: https://arxiv.org/abs/2405.11234
- **BibTeX Key**: `bitton2024winoground`

## Abstract
Vision-Language Models often appear to succeed on visual QA by exploiting language priors rather than grounding true compositionality. In this paper, we probe spatial prepositions and compositionality in modern VLMs using counterfactual image-text pairs where objects swap spatial configurations (e.g. 'the cat is on the mat' vs 'the mat is on the cat'). We find that models show severe compositional vulnerabilities, frequently failing to differentiate reversed spatial prepositions despite correctly identifying both entities in isolation.

## Key Extracted Contributions
1. VLMs correctly identify individual object nouns but fail to ground the spatial prepositions connecting them.
2. When two target entities are present, the model often randomly assigns directional prepositions.
3. Confirms that bag-of-words text associations dominate attention over visual spatial geometry.
