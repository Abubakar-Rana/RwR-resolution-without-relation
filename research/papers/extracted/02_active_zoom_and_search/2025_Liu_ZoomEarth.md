# Machine Extraction: ZoomEarth: Active Perception for Ultra-High-Resolution Geospatial Vision-Language Tasks

- **BibTeX Key**: `liu2025zoomearth`
- **Authors**: Rui Liu, Fangrun Wang, Haoliang Wang, Wen Yang
- **Venue**: arXiv preprint (2025)
- **arXiv**: [2502.19011](https://arxiv.org/abs/2502.19011)
- **Code**: https://github.com/WHU-USI/ZoomEarth
- **Category**: 02_active_zoom_and_search
- **Relevance**: 5 / 5 (Critical Direct Baseline)

## Abstract
Fixed tiling strategies waste compute on uninformative background patches and shatter scene topology. ZoomEarth treats gigapixel image comprehension as an active perception task, training a policy model to iteratively zoom, pan, and focus on relevant regions guided by the query.

## Key Empirical Findings
1. Active zooming cuts token budget by 65% compared to uniform tiling.
2. Achieves high accuracy on fine object recognition but incurs multi-step inference latency.
3. Search policy occasionally gets trapped in local visual distractors.

## Authors' Stated Conclusions
Question-conditioned active search outperforms uniform grid slicing in token efficiency.

## Open Challenges & Future Scope
Single-step multi-scale routing and reducing sequential search latency.

## Architectural Profile
- **Vision**: CLIP ViT-L/14 with Dynamic Affine Crop
- **Projector**: MLP
- **LLM**: Qwen2-VL-7B
- **Tokens**: 1,200 tokens per step (up to 5 steps)
