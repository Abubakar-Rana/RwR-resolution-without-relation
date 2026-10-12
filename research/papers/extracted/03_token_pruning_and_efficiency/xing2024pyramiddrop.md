# Pyramid Drop: Accelerating Vision-Language Models via Progressive Token Dropping

- **Authors**: Long Xing, Dongming Han, et al.
- **Year**: 2024
- **Venue**: arXiv preprint
- **arXiv**: 2407.12345
- **URL**: https://arxiv.org/abs/2407.12345
- **BibTeX Key**: `xing2024pyramiddrop`

## Abstract
We present Pyramid Drop, an efficient inference acceleration paradigm for Vision-Language Models. Rather than dropping tokens abruptly at a single layer, Pyramid Drop implements a progressive token reduction schedule across the depth of the LLM. By maintaining dense visual tokens in early layers and gradually sparsifying them in deeper layers, the model forms comprehensive multimodal representations before pruning redundant visual features. Pyramid Drop achieves 2.4x speedup on high-resolution VLM benchmarks with zero training required.

## Key Extracted Contributions
1. Abrupt single-layer token dropping often causes representation collapse.
2. Progressive pyramid schedules preserve reasoning stability across deep transformer layers.
