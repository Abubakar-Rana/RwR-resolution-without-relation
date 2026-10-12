# Machine Extraction: Adaptive Resolution for Vision-Language Models

- **BibTeX Key**: `yuan2024adaptiveres`
- **Authors**: Hao Yuan, Jianfei Gao, Siyuan Li
- **Venue**: arXiv preprint (2024)
- **arXiv**: [2405.18900](https://arxiv.org/abs/2405.18900)
- **Code**: https://github.com/YuanHao/AdaptiveRes
- **Category**: 06_routing_and_cascading
- **Relevance**: 4 / 5 (High Architectural Prior)

## Abstract
Different visual tasks require drastically different image resolutions. AdaptiveRes trains a query classifier that predicts the minimum required visual resolution for a given query, dispatching OCR and fine detail queries to high resolution while routing scene classification and spatial queries to low resolution.

## Key Empirical Findings
1. Text query semantics strongly predict the required visual resolution.
2. Spatial orientation and scene-level queries perform optimally at lower resolutions with broader field of view.
3. Saves 55% FLOPs across VQA benchmarks with zero accuracy loss.

## Authors' Stated Conclusions
Query semantics provide a powerful inductive prior for determining required visual resolution.

## Open Challenges & Future Scope
Joint resolution and crop region selection.

## Architectural Profile
- **Vision**: Dynamic ViT (224 to 1024)
- **Projector**: MLP
- **LLM**: LLaMA-3-8B
- **Tokens**: Variable (196 to 4,096 tokens)
