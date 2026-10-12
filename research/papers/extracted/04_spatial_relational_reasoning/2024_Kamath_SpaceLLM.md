# Machine Extraction: SpaceLLM: Spatial Reasoning and Coordinate Grounding for 2D/3D Multimodal LLMs

- **BibTeX Key**: `kamath2024spacellm`
- **Authors**: Amita Kamath, Christopher Clark, Tanmay Gupta, Eric Kolve, Derek Hoiem, Aniruddha Kembhavi
- **Venue**: ECCV 2024 (2024)
- **arXiv**: [2404.14405](https://arxiv.org/abs/2404.14405)
- **Code**: https://github.com/allenai/SpaceLLM
- **Category**: 04_spatial_relational_reasoning
- **Relevance**: 4 / 5 (High Spatial Prior)

## Abstract
We introduce SpaceLLM, designed to reason about 2D and 3D spatial configurations. By integrating continuous coordinate prediction and specialized spatial loss functions, SpaceLLM masters directional prepositions, distance comparisons, and relative object orientations.

## Key Empirical Findings
1. Continuous coordinate supervision improves relational spatial reasoning by +15.3%.
2. Discloses that standard cross-entropy loss on discretized coordinate tokens causes quantization errors on distances.
3. Directional reasoning requires explicit spatial vector alignment.

## Authors' Stated Conclusions
Discretized text tokens are a poor representation for continuous spatial coordinates; continuous loss is superior.

## Open Challenges & Future Scope
Scaling to ultra-high-resolution aerial imagery.

## Architectural Profile
- **Vision**: CLIP ViT-L/14 with Spatial Heads
- **Projector**: MLP + Continuous Coordinate Head
- **LLM**: Vicuna-7B
- **Tokens**: 576 tokens
