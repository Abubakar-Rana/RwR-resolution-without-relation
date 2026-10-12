# Machine Extraction: DynamicViT: Efficient Vision Transformers with Dynamic Token Sparsification

- **BibTeX Key**: `rao2021dynamicvit`
- **Authors**: Yongming Rao, Wenliang Zhao, Benlin Liu, Jiwen Lu, Jie Zhou, Cho-Jui Hsieh
- **Venue**: NeurIPS 2021 (2021)
- **arXiv**: [2106.02030](https://arxiv.org/abs/2106.02030)
- **Code**: https://github.com/raoyongming/DynamicViT
- **Category**: 06_routing_and_cascading
- **Relevance**: 4 / 5 (Foundational Dynamic Routing)

## Abstract
We propose DynamicViT, a dynamic token sparsification framework for Vision Transformers. Lightweight prediction heads prune uninformative visual tokens progressively across transformer stages, reducing FLOPs by 48% with <0.5% accuracy drop.

## Key Empirical Findings
1. Gumbel-Softmax training enables end-to-end learning of discrete token routing decisions.
2. Pruning 50% of tokens causes virtually zero accuracy loss on ImageNet.
3. Visual redundancy is concentrated in background regions.

## Authors' Stated Conclusions
Dynamic instance-specific token routing significantly outperforms static uniform token budgets.

## Open Challenges & Future Scope
Multimodal cross-attention routing.

## Architectural Profile
- **Vision**: DeiT-S / DeiT-B with Dynamic Routing Heads
- **Projector**: N/A
- **LLM**: None
- **Tokens**: Pruned dynamically
