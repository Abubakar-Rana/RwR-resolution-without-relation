# Machine Extraction: REVERIE: Remote Embodied Visual Referring Expression in Real Indoor Environments

- **BibTeX Key**: `qi2024reverie`
- **Authors**: Yuankai Qi, Qi Wu, Peter Anderson, Xin Wang, William Yang Wang, Shenghua Gao, Ming-Hsuan Yang
- **Venue**: CVPR 2020 (2020)
- **arXiv**: [1904.10151](https://arxiv.org/abs/1904.10151)
- **Code**: https://github.com/YuankaiQi/REVERIE
- **Category**: 09_embodied_and_3d_spatial_priors
- **Relevance**: 3 / 5 (Moderate Referring Prior)

## Abstract
We introduce REVERIE, a benchmark requiring agents to navigate to a distant room and ground a specific target object described by high-level instructions (e.g. 'bring me the blue mug on the kitchen table').

## Key Empirical Findings
1. High-level instructions require joint navigation planning and object grounding.
2. Object grounding success drops severely when the agent stops in sub-optimal viewing positions.
3. Identifies the interplay between viewpoint selection and object recognition.

## Authors' Stated Conclusions
Viewing position and camera angle determine visual grounding success in complex physical spaces.

## Open Challenges & Future Scope
Active camera repositioning for grounding.

## Architectural Profile
- **Vision**: Faster R-CNN + ResNet-152
- **Projector**: Cross-modal attention
- **LLM**: None (Pre-LLM era)
- **Tokens**: N/A
