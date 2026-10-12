# Machine Extraction: SpatialNav: Cardinal Reasoning and Obstacle Mapping in VLMs

- **BibTeX Key**: `chen2024spatialnav`
- **Authors**: Boyuan Chen, Sean Kirmani, Brian Ichter, Danny Driess
- **Venue**: ICRA 2024 (2024)
- **arXiv**: [2402.13890](https://arxiv.org/abs/2402.13890)
- **Code**: https://spatial-nav.github.io
- **Category**: 09_embodied_and_3d_spatial_priors
- **Relevance**: 4 / 5 (High Spatial Prior)

## Abstract
First-person perspective creates severe visual occlusion that impairs spatial planning. SpatialNav converts first-person observations into top-down 2D orthographic cost maps, training VLMs to perform cardinal reasoning and obstacle avoidance directly on 2D layouts.

## Key Empirical Findings
1. Top-down orthographic 2D maps improve spatial reasoning and obstacle avoidance by +34% over ego-centric views.
2. Eliminates perspective foreshortening and hidden surface occlusions.
3. Directly mirrors overhead remote sensing perspective.

## Authors' Stated Conclusions
Top-down orthographic 2D maps provide the most effective geometric representation for spatial reasoning in neural models.

## Open Challenges & Future Scope
Gigapixel scale map reasoning.

## Architectural Profile
- **Vision**: ViT-L/14 Top-Down Map Encoder
- **Projector**: MLP
- **LLM**: PaLM-2
- **Tokens**: 576 tokens
