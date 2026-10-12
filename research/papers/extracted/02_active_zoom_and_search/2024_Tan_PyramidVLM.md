# Machine Extraction: PyramidVLM: Hierarchical Pyramid Features for High-Resolution Vision-Language

- **BibTeX Key**: `tan2024pyramidvlm`
- **Authors**: Sinan Tan, Jinze Bai, Shusheng Yang, Junyang Lin
- **Venue**: arXiv preprint (2024)
- **arXiv**: [2408.14205](https://arxiv.org/abs/2408.14205)
- **Code**: https://github.com/Alibaba-NLP/PyramidVLM
- **Category**: 02_active_zoom_and_search
- **Relevance**: 4 / 5 (High Architectural Prior)

## Abstract
We introduce PyramidVLM, incorporating a Feature Pyramid Network into the cross-modal projector. By performing top-down feature fusion across visual pyramid levels, PyramidVLM endows visual tokens with both fine detail and global context.

## Key Empirical Findings
1. Top-down feature fusion improves spatial relationship accuracy by +6.5% over independent tiling.
2. Preserves coordinate awareness across scales.
3. Requires custom projector architecture.

## Authors' Stated Conclusions
Feature pyramid fusion in the projector bridges the gap between local crops and global layout.

## Open Challenges & Future Scope
Generalizing pyramid fusion to training-free test-time wrappers.

## Architectural Profile
- **Vision**: ViT-H/14 with 3-level FPN
- **Projector**: Top-down FPN Resampler
- **LLM**: Qwen-7B
- **Tokens**: 1,024 tokens
