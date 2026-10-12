# Machine Extraction: GeoEmbodied: Autonomous Drone Navigation via Grounded Multimodal Foundation Models

- **BibTeX Key**: `liu2025geoembodiedagent`
- **Authors**: Rui Liu, Fangrun Wang, Haoliang Wang, Wen Yang
- **Venue**: CVPR 2025 (2025)
- **arXiv**: [2502.19890](https://arxiv.org/abs/2502.19890)
- **Code**: https://github.com/WHU-USI/GeoEmbodied
- **Category**: 09_embodied_and_3d_spatial_priors
- **Relevance**: 5 / 5 (Critical Direct Comparison)

## Abstract
We present GeoEmbodied, an autonomous drone navigation framework powered by multimodal foundation models. GeoEmbodied combines hierarchical visual search over gigapixel orthophotos with real-time open-vocabulary target grounding and topological route planning.

## Key Empirical Findings
1. Decomposing drone navigation into global topological planning and local zoom verification achieves 92.4% mission success.
2. Preserves global cardinal reference points on massive 8K orthophotos.
3. Integrates YOLO-based open-vocabulary candidate proposal with VLM semantic decision making.

## Authors' Stated Conclusions
Hierarchical visual search paired with real-time open-vocabulary detectors provides the optimal framework for aerial multimodal navigation.

## Open Challenges & Future Scope
Multi-drone collaborative exploration.

## Architectural Profile
- **Vision**: YOLO-World + Qwen2-VL
- **Projector**: Topological Router
- **LLM**: Qwen2-7B-Instruct
- **Tokens**: Variable
