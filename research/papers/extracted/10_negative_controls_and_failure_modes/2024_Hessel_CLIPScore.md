# Machine Extraction: CLIPScore: Reference-Free Evaluation and Its Blind Spots

- **BibTeX Key**: `hessel2024clipscore`
- **Authors**: Jack Hessel, Ari Holtzman, Maxwell Forbes, Ronan Le Bras, Yejin Choi
- **Venue**: EMNLP 2021 (2021)
- **arXiv**: [2104.08718](https://arxiv.org/abs/2104.08718)
- **Code**: https://github.com/jmhessel/clipscore
- **Category**: 10_negative_controls_and_failure_modes
- **Relevance**: 3 / 5 (Metric Blindspot Analysis)

## Abstract
We present CLIPScore, a reference-free metric for image caption evaluation. While CLIPScore correlates strongly with human judgment on semantic relevance, we identify critical blind spots: CLIPScore fails to penalize incorrect object counts or inverted spatial relationships.

## Key Empirical Findings
1. CLIPScore cannot detect counting errors (hallucinating 5 cars instead of 2 yields high score).
2. Blind to spatial relation inversions ('above' vs 'below').
3. Warns against using CLIP-based metrics for spatial evaluation.

## Authors' Stated Conclusions
CLIP-based similarity scores must not be used as evaluators for spatial relations or object counts.

## Open Challenges & Future Scope
Compositional metrics.

## Architectural Profile
- **Vision**: CLIP ViT-B/32
- **Projector**: Cosine similarity
- **LLM**: None
- **Tokens**: Global pooled vector
