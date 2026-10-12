# Machine Extraction: Eyes Wide Shut? Exploring the Visual Spatial Reasoning Limits of Multi-Modal Large Language Models

- **BibTeX Key**: `tong2024eyeswideshut`
- **Authors**: Shengbang Tong, Zhuang Liu, Yuexiang Zhai, Yi Ma, Yann LeCun
- **Venue**: CVPR 2024 (2024)
- **arXiv**: [2403.02151](https://arxiv.org/abs/2403.02151)
- **Code**: https://github.com/ShengbangTong/EyesWideShut
- **Category**: 04_spatial_relational_reasoning
- **Relevance**: 4 / 5 (High Spatial Prior)

## Abstract
Why do advanced MLLMs struggle with basic visual spatial tasks? We trace this weakness directly to the visual encoder. We show that contrastive pretraining (CLIP) collapses fine spatial structures in favor of high-level semantic abstractions, leaving downstream LLMs without the spatial signals necessary for relational reasoning.

## Key Empirical Findings
1. CLIP visual tokens lose spatial coordinate fidelity in deeper layers as semantic invariant loss dominates.
2. Visual token representations cannot reconstruct relative distance or orientation without retraining.
3. Supervised self-attention heads prioritize object identity over inter-object spatial vectors.

## Authors' Stated Conclusions
The root cause of spatial reasoning failure lies in the visual encoder pretraining objective, which optimizes for semantic invariance rather than spatial equivariance.

## Open Challenges & Future Scope
Spatially equivariant vision-language foundation models.

## Architectural Profile
- **Vision**: CLIP ViT-L/14, DINOv2, SigLIP
- **Projector**: MLP
- **LLM**: LLaVA-1.5-7B / GPT-4V
- **Tokens**: 576 tokens
