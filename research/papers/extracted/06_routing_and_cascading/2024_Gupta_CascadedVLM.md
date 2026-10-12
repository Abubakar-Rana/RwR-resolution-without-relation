# Machine Extraction: Cascaded Vision-Language Models for Efficient High-Resolution Video and Image Understanding

- **BibTeX Key**: `gupta2024cascadedvlm`
- **Authors**: Tanmay Gupta, Amita Kamath, Aniruddha Kembhavi
- **Venue**: CVPR 2024 (2024)
- **arXiv**: [2404.09112](https://arxiv.org/abs/2404.09112)
- **Code**: https://github.com/allenai/CascadedVLM
- **Category**: 06_routing_and_cascading
- **Relevance**: 4 / 5 (High Architectural Prior)

## Abstract
High-resolution video and image VQA suffer extreme compute costs. We introduce CascadedVLM, a multi-tier cascade where a 2B model scans coarse frames/crops and escalates ambiguous queries to a 13B model. CascadedVLM cuts inference cost by 68% while matching 13B accuracy.

## Key Empirical Findings
1. Multi-tier cascades achieve the accuracy of the large model at the average latency of the small model.
2. Entropy gating reliably predicts when the lightweight model's answer is trustworthy.
3. Effective for multi-crop image understanding.

## Authors' Stated Conclusions
Cascaded evaluation across model scales and visual resolutions achieves superior throughput without accuracy compromise.

## Open Challenges & Future Scope
Joint spatial and temporal gating.

## Architectural Profile
- **Vision**: CLIP ViT-L/14 (Multi-scale)
- **Projector**: MLP
- **LLM**: Tier 1: Gemma-2B / Tier 2: LLaMA-3-8B
- **Tokens**: Variable
