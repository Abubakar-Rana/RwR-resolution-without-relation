# Machine Extraction: When Large Vision-Language Model Meets Large Remote Sensing Imagery: Coarse-to-Fine Text-Guided Token Pruning

- **BibTeX Key**: `luo2025lrsvqa`
- **Authors**: Jiaqi Luo, Dong Wang, Zichen Guo, Wen Yang
- **Venue**: CVPR 2025 (2025)
- **arXiv**: [2502.13456](https://arxiv.org/abs/2502.13456)
- **Code**: https://github.com/WHU-USI/LRS-VQA
- **Category**: 03_token_pruning_and_efficiency
- **Relevance**: 5 / 5 (Critical Efficiency Prior)

## Abstract
Applying MLLMs to massive remote sensing imagery incurs prohibitive computational costs due to excessive visual tokens. We introduce LRS-VQA, a text-guided token pruning framework that progressively evaluates patch relevance against the textual query across transformer layers, discarding uninformative background patches while preserving multi-scale target tokens.

## Key Empirical Findings
1. Up to 80% of visual tokens in remote sensing images correspond to uniform background (grass, ocean, desert) and can be safely dropped.
2. Text-guided cross-attention identifies query-relevant patches with high precision.
3. Reduces inference latency by 3.8x and memory by 65% with <0.8% accuracy drop.

## Authors' Stated Conclusions
Text-guided visual token pruning resolves the computational bottleneck of high-resolution remote sensing MLLMs.

## Open Challenges & Future Scope
Adapting pruning to preserve relational context tokens between distant objects.

## Architectural Profile
- **Vision**: SigLIP-SO400M with Cross-Attention Pruning
- **Projector**: MLP
- **LLM**: Qwen2-7B-Instruct
- **Tokens**: Variable (Pruned from 4,096 to 819 tokens)
