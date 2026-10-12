# Machine Extraction: MoE-LLaVA: Mixture of Experts for Large Vision-Language Models

- **BibTeX Key**: `lin2024moellava`
- **Authors**: Bin Lin, Zhenyu Tang, Yang Ye, Jiaxi Cui, Bin Zhu, Peng Jin, Junwu Zhang, Munan Ning, Li Yuan
- **Venue**: arXiv preprint (2024)
- **arXiv**: [2401.15947](https://arxiv.org/abs/2401.15947)
- **Code**: https://github.com/PKU-YuanGroup/MoE-LLaVA
- **Category**: 06_routing_and_cascading
- **Relevance**: 4 / 5 (High Architectural Prior)

## Abstract
We present MoE-LLaVA, a sparse mixture-of-experts architecture for multimodal LLMs. By replacing standard feed-forward networks with sparse MoE layers, MoE-LLaVA dynamically activates only top-k experts per token, scaling model capacity with constant compute.

## Key Empirical Findings
1. Sparse MoE activates only 2.2B to 3.0B parameters per token, reducing inference latency by 3x.
2. Discovers expert specialization: distinct experts specialize in visual geometry vs linguistic semantics.
3. Routing tokens through specialized visual experts improves fine-grained grounding.

## Authors' Stated Conclusions
Sparse routing across specialized expert networks scales multimodal capacity without increasing inference cost.

## Open Challenges & Future Scope
Routing at the sequence level and resolution level.

## Architectural Profile
- **Vision**: CLIP ViT-L/14-336
- **Projector**: MLP
- **LLM**: MoE-LLaVA (16 experts, top-2 activated)
- **Tokens**: 576 tokens
