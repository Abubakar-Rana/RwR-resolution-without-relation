# Machine Extraction: Pyramid Drop: Accelerating Vision-Language Models via Progressive Token Dropping

- **BibTeX Key**: `xing2024pyramiddrop`
- **Authors**: Long Xing, Dong Wang, Zichen Guo, Wen Yang
- **Venue**: arXiv preprint (2024)
- **arXiv**: [2408.08922](https://arxiv.org/abs/2408.08922)
- **Code**: https://github.com/WHU-USI/PyramidDrop
- **Category**: 03_token_pruning_and_efficiency
- **Relevance**: 3 / 5 (Moderate Efficiency Prior)

## Abstract
Abrupt token pruning at early layers causes irreversible information loss. PyramidDrop introduces progressive token dropping across transformer layers, gradually thinning visual tokens as semantic abstraction deepens.

## Key Empirical Findings
1. Progressive layer-wise dropping preserves nuanced relationships better than single-layer hard pruning.
2. Achieves 2.5x speedup with less than 0.5% accuracy degradation on standard benchmarks.
3. Preserves multi-hop reasoning pathways.

## Authors' Stated Conclusions
Progressive multi-stage token dropping stabilizes deep visual-linguistic reasoning.

## Open Challenges & Future Scope
Hardware-aligned sparse kernels for variable sequence lengths.

## Architectural Profile
- **Vision**: CLIP ViT-L/14
- **Projector**: MLP
- **LLM**: Llama-3-8B-Instruct
- **Tokens**: Thinned from 576 to 144 across 32 layers
