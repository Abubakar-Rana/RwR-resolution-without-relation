# Machine Extraction: RelationalVLM: Explicit Spatial Relations via Positional Encodings

- **BibTeX Key**: `yuan2024relationalvlm`
- **Authors**: Hao Yuan, Jianfei Gao, Siyuan Li
- **Venue**: NeurIPS 2024 (2024)
- **arXiv**: [2408.15234](https://arxiv.org/abs/2408.15234)
- **Code**: https://github.com/YuanHao/RelationalVLM
- **Category**: 04_spatial_relational_reasoning
- **Relevance**: 4 / 5 (High Architectural Prior)

## Abstract
Vision-language models rely on 1D or basic 2D positional encodings that fail to represent directional vectors between entities. RelationalVLM introduces Relative Spatial Position Encoding (RSPE), directly modulating attention logits by relative displacement vectors.

## Key Empirical Findings
1. RSPE improves spatial relation accuracy by +14.6% on CLEVR and GQA.
2. Preserves cardinal orientation under rotation.
3. Modulates self-attention weights directly with Euclidean displacement vectors.

## Authors' Stated Conclusions
Directly encoding pairwise displacement vectors into self-attention eliminates spatial disorientation.

## Open Challenges & Future Scope
Extending to multi-crop tiled inputs.

## Architectural Profile
- **Vision**: ViT-L/14 with RSPE Attention
- **Projector**: MLP
- **LLM**: Vicuna-7B
- **Tokens**: 576 tokens
