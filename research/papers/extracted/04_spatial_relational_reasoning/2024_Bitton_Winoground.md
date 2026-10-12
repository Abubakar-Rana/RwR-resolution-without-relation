# Machine Extraction: Beyond Winoground: Probing Spatial Prepositions and Compositionality in VLMs

- **BibTeX Key**: `bitton2024winoground`
- **Authors**: Yonatan Bitton, Hadas Orgad, Pradeep Dasigi, Gabriel Stanovsky, Roy Schwartz
- **Venue**: ACL 2024 (2024)
- **arXiv**: [2403.07840](https://arxiv.org/abs/2403.07840)
- **Code**: https://github.com/yonatanbitton/beyond-winoground
- **Category**: 04_spatial_relational_reasoning
- **Relevance**: 3 / 5 (Moderate Linguistic Prior)

## Abstract
We evaluate whether vision-language models truly understand spatial prepositions or merely rely on lexical frequencies. Using carefully balanced minimal pairs where swapping prepositions reverses ground truth, we demonstrate that most VLMs exhibit near-chance compositional accuracy.

## Key Empirical Findings
1. Swapping spatial prepositions drops VLM accuracy to 28.5% (chance = 25%).
2. Attention maps show models ignore preposition tokens during visual cross-attention.
3. Pretrained representations do not bind spatial relation words to physical visual geometry.

## Authors' Stated Conclusions
Vision-language alignment is heavily biased toward nouns and attributes, treating prepositions as ungrounded noise.

## Open Challenges & Future Scope
Compositional contrastive pretraining.

## Architectural Profile
- **Vision**: CLIP ViT-B/32 & ViT-L/14
- **Projector**: Linear
- **LLM**: None (Contrastive scoring)
- **Tokens**: N/A
