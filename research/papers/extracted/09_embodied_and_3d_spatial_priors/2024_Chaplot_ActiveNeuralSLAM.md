# Machine Extraction: Learning To Explore Using Active Neural SLAM

- **BibTeX Key**: `chaplot2024activeneuralslam`
- **Authors**: Devendra Singh Chaplot, Dhiraj Gandhi, Saurabh Gupta, Abhinav Gupta, Ruslan Salakhutdinov
- **Venue**: ICLR 2020 (2020)
- **arXiv**: [2004.00644](https://arxiv.org/abs/2004.00644)
- **Code**: https://github.com/devendrachaplot/Neural-SLAM
- **Category**: 09_embodied_and_3d_spatial_priors
- **Relevance**: 4 / 5 (High SLAM Prior)

## Abstract
We present Active Neural SLAM, an approach for exploring unseen environments. It builds an internal top-down 2D occupancy map using neural SLAM and selects long-term exploration goals using an analytical planner, achieving efficient coverage.

## Key Empirical Findings
1. Decoupling spatial mapping (neural) from path planning (analytical) vastly outperforms end-to-end RL.
2. Explicit 2D occupancy grids eliminate map hallucination.
3. Reaches 95% exploration coverage 3x faster than monolithic models.

## Authors' Stated Conclusions
Separating perceptual spatial mapping from analytical path planning is the optimal architecture for spatial navigation.

## Open Challenges & Future Scope
Semantic multi-class spatial mapping.

## Architectural Profile
- **Vision**: ResNet-18 Neural Mapper
- **Projector**: 2D Occupancy Grid
- **LLM**: Analytical Fast Marching Method (FMM)
- **Tokens**: Grid cells
