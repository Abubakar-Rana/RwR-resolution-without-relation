# ZoomEarth: Active Perception for Ultra-High-Resolution Geospatial Vision-Language Tasks

- **Authors**: Rui Liu, Bo Fu, Junbo Song, Kai Li, Wei Li, Lin Xue, Hongsheng Qiao, Weidong Zhang, Deyu Meng, Xuelong Cao
- **Year**: 2025
- **Venue**: arXiv preprint
- **arXiv**: 2511.12267
- **URL**: https://arxiv.org/abs/2511.12267
- **BibTeX Key**: `liu2025zoomearth`

## Abstract
Interpreting gigapixel remote sensing scenes requires human-like active perception, where observers iteratively glance at global context and zoom into critical details. We present ZoomEarth, an active perception framework for ultra-high-resolution geospatial vision-language tasks. ZoomEarth models high-resolution image interpretation as a sequential decision-making process: an active policy network observes low-resolution overviews, selects task-relevant crops, and updates an internal visual memory. Experimental evaluations on XLRS-Bench and UHR benchmarks demonstrate that ZoomEarth achieves significant gains on small-target recognition compared to passive uniform tiling, though at the expense of sequential step latency.

## Key Extracted Contributions
1. Uniform tiling wastes over 80% of compute on empty background tiles.
2. Reinforcement-learned active zooming focuses effectively on query-relevant infrastructure.
3. Multi-step zooming introduces sequential inference bottlenecks (averaging 4-6 sequential VLM calls per query).
