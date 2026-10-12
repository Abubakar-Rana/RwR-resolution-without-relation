# An Image is Worth 1/2 Tokens After Layer 2: Plug-and-Play Sparse Auto-Encoders for Efficient Vision-Language Models (FastV)

- **Authors**: Liang Chen, Haozhe Zhao, Jian Guan, et al.
- **Year**: 2024
- **Venue**: ECCV 2024
- **arXiv**: 2403.06764
- **URL**: https://arxiv.org/abs/2403.06764
- **BibTeX Key**: `chen2024fastv`

## Abstract
Large Vision-Language Models incur heavy quadratic computational costs as visual token counts grow. In this paper, we conduct an empirical analysis of attention distribution in LVLMs and discover an intriguing phenomenon: visual tokens receive substantial attention in early LLM layers, but attention rapidly concentrates on a few anchor tokens and punctuation in deeper layers. Based on this observation, we propose FastV, a training-free plug-and-play visual token pruning strategy. FastV evaluates visual token attention weights at layer K (e.g. layer 2) and drops the bottom 50% to 75% of visual tokens for all subsequent layers. Extensive experiments demonstrate that FastV cuts FLOPs by 45% and improves inference speed by up to 2x without requiring retraining.

## Key Extracted Contributions
1. Attention to visual tokens decays precipitously after the first 2-3 layers of decoder-only LLMs.
2. Dropping 50% of visual tokens after layer 2 preserves over 98% of benchmark performance.
3. Completely training-free and compatible with LLaVA, Qwen-VL, and other autoregressive models.
