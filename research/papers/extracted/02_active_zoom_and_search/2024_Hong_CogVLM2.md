# Machine Extraction: CogVLM2: Visual Language Model with High Resolution Support

- **BibTeX Key**: `hong2024cogvlm2`
- **Authors**: Wenyi Hong, Weihan Wang, Qingsong Lv, Jiale Cheng, Yanbo Xu
- **Venue**: arXiv preprint (2024)
- **arXiv**: [2408.16500](https://arxiv.org/abs/2408.16500)
- **Code**: https://github.com/THUDM/CogVLM2
- **Category**: 02_active_zoom_and_search
- **Relevance**: 3 / 5 (Moderate Architectural Prior)

## Abstract
We present CogVLM2, enhancing visual language understanding through dedicated visual expert blocks and high-resolution input support. Deep visual-language fusion enables superior spatial localization and detail perception.

## Key Empirical Findings
1. Deep expert fusion outperforms shallow MLP projectors on fine-grained grounding.
2. Computational overhead scales substantially with input resolution.

## Authors' Stated Conclusions
Deep visual-language fusion improves coordinate grounding at high compute cost.

## Open Challenges & Future Scope
Sparser token routing through visual expert layers.

## Architectural Profile
- **Vision**: EVA-02-CLIP-E/14
- **Projector**: Deep Visual Expert Layers
- **LLM**: GLM-4-9B
- **Tokens**: 2,048 tokens
