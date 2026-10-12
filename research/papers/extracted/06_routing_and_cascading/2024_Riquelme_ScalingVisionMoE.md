# Machine Extraction: Scaling Vision with Sparse Mixture of Experts

- **BibTeX Key**: `riquelme2024scalingvisionmoe`
- **Authors**: Carlos Riquelme, Joan Puigcerver, Basil Mustafa, Cedric Renggli, Andre Susano Pinto, Sylvain Gelly, Daniel Keysers, Neil Houlsby
- **Venue**: NeurIPS 2021 (2021)
- **arXiv**: [2106.05974](https://arxiv.org/abs/2106.05974)
- **Code**: https://github.com/google-research/vmoe
- **Category**: 06_routing_and_cascading
- **Relevance**: 4 / 5 (Foundational Vision MoE)

## Abstract
We present V-MoE, a sparse Mixture of Experts architecture for vision. V-MoE routes image patch tokens through sparse expert layers, demonstrating that visual routing naturally clusters patches by semantic content and spatial frequency.

## Key Empirical Findings
1. Sparse routing scales vision models to 15B parameters effectively.
2. Routing heads naturally separate foreground targets from background terrain.
3. Priority routing discards excess background patch tokens gracefully.

## Authors' Stated Conclusions
Visual tokens exhibit high routing sparsity; background patches require far less capacity than foreground entities.

## Open Challenges & Future Scope
Multimodal vision-language MoE scaling.

## Architectural Profile
- **Vision**: V-MoE (ViT-H/14 with 32 experts)
- **Projector**: N/A
- **LLM**: None
- **Tokens**: Sparse patch routing
