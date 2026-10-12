# Machine Extraction: SpatialVLM: Endowing Vision-Language Models with Spatial Reasoning Capabilities

- **BibTeX Key**: `chen2024spatialvlm`
- **Authors**: Boyuan Chen, Zhuo Xu, Sean Kirmani, Brian Ichter, Danny Driess, Fei Xia
- **Venue**: CVPR 2024 (2024)
- **arXiv**: [2401.12168](https://arxiv.org/abs/2401.12168)
- **Code**: https://spatial-vlm.github.io
- **Category**: 04_spatial_relational_reasoning
- **Relevance**: 5 / 5 (Critical Spatial Prior)

## Abstract
We present SpatialVLM, endowing vision-language models with quantitative and qualitative spatial reasoning capabilities. By generating a synthetic dataset of 2 billion spatial VQA pairs using 3D spatial annotations, SpatialVLM teaches VLMs metric distances, cardinal directions, and relative spatial reasoning.

## Key Empirical Findings
1. Standard VLMs (PaLM-E, GPT-4V) perform near chance on metric distance estimation and spatial relations.
2. Explicit spatial supervision on 2D/3D coordinate pairs enables robust relational reasoning.
3. Spatial knowledge transfers to downstream robotic navigation and complex spatial reasoning.

## Authors' Stated Conclusions
Spatial reasoning does not emerge spontaneously from internet-scale image-text pretraining; it requires explicit spatial grounding supervision.

## Open Challenges & Future Scope
Generalizing spatial representations to ultra-high-resolution aerial domains.

## Architectural Profile
- **Vision**: PaLI-X Vision Encoder (ViT-22B)
- **Projector**: Linear
- **LLM**: PaLM-2
- **Tokens**: 1,024 tokens
