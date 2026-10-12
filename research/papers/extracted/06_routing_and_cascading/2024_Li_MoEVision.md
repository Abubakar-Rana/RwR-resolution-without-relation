# Machine Extraction: MoE-Vision: Dynamic Routing Across Modalities and Resolutions

- **BibTeX Key**: `li2024moevision`
- **Authors**: Yuan Li, Hao Zhang, Mengdi Li, Jiayan Teng
- **Venue**: CVPR 2024 (2024)
- **arXiv**: [2404.18210](https://arxiv.org/abs/2404.18210)
- **Code**: https://github.com/THU-Li/MoE-Vision
- **Category**: 06_routing_and_cascading
- **Relevance**: 4 / 5 (High Architectural Prior)

## Abstract
We introduce MoE-Vision, dynamically routing visual tokens across multi-resolution encoder pathways. High-gradient and query-relevant tokens route through high-resolution experts, while low-frequency background routes through low-resolution experts.

## Key Empirical Findings
1. Multi-resolution expert routing reduces visual token sequence length by 60%.
2. Preserves fine-grained perception on text and small objects.
3. Balances compute across heterogeneous image regions.

## Authors' Stated Conclusions
Routing visual tokens by spatial frequency and query relevance yields Pareto-optimal visual representations.

## Open Challenges & Future Scope
Generalizing to gigapixel aerial images.

## Architectural Profile
- **Vision**: Multi-Resolution ViT (Dual scale)
- **Projector**: MoE Projector (4 resolution experts)
- **LLM**: Vicuna-7B
- **Tokens**: Variable (60% reduction)
