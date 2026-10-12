# Machine Extraction: Dynamic High-Resolution Vision Transformer for Multi-Scale Vision-Language

- **BibTeX Key**: `yuan2024dynamichighres`
- **Authors**: Hao Yuan, Zhengyi Wang, Jianfei Gao
- **Venue**: ECCV 2024 (2024)
- **arXiv**: [2407.18901](https://arxiv.org/abs/2407.18901)
- **Code**: https://github.com/YuanHao/DynamicHR-ViT
- **Category**: 02_active_zoom_and_search
- **Relevance**: 3 / 5 (Moderate Prior)

## Abstract
Not all image regions require high resolution. We develop a dynamic resolution transformer that allocates high-resolution tokens only to high-entropy, question-relevant visual patches while subsampling uniform background.

## Key Empirical Findings
1. Visual entropy + text attention identifies 90% of relevant targets.
2. Cuts visual tokens by 60% with negligible loss in accuracy.

## Authors' Stated Conclusions
Selective token allocation is far more efficient than uniform dense grids.

## Open Challenges & Future Scope
Integration into open-weights multimodal foundation models.

## Architectural Profile
- **Vision**: Dynamic HR-ViT-L
- **Projector**: Linear
- **LLM**: None
- **Tokens**: Variable
