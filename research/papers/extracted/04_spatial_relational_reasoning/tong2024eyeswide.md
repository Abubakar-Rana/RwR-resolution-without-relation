# Eyes Wide Shut? Exploring the Visual Spatial Reasoning Limits of Multi-Modal Large Language Models

- **Authors**: Shengbang Tong, Ellis Brown, Boyuan Chen, et al.
- **Year**: 2024
- **Venue**: CVPR 2024
- **arXiv**: 2403.09876
- **URL**: https://arxiv.org/abs/2403.09876
- **BibTeX Key**: `tong2024eyeswide`

## Abstract
Does scaling up language backbones in Multimodal Large Language Models (MLLMs) automatically resolve spatial reasoning shortcomings? In this paper, we conduct a systematic evaluation of spatial reasoning across model scales from 3B to 70B parameters. We find that while scaling LLMs dramatically improves high-level knowledge and reasoning chains, it yields almost negligible improvements on basic visual spatial relations (e.g. relative position, counting, boundary touching). We demonstrate that the bottleneck resides in the visual representations produced by standard vision backbones, which discard fine-grained spatial coordinates during patch pooling.

## Key Extracted Contributions
1. Scaling LLM parameters from 7B to 70B yields <3% gain on spatial relational tasks.
2. Spatial reasoning is fundamentally bounded by the visual encoder and projector representations, not language model reasoning capacity.
3. Upgrading the vision projector and coordinate representation yields far greater gains than scaling model parameters.
