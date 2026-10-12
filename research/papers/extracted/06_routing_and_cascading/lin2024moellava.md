# MoE-LLaVA: Mixture of Experts for Large Vision-Language Models

- **Authors**: Bin Lin, Zhenyu Tang, Yang Ye, Jiaxi Cui, Bin Wang, Peng Jin, Junwu Zhang, Munan Ning, Li Yuan
- **Year**: 2024
- **Venue**: CVPR 2024
- **arXiv**: 2401.15947
- **URL**: https://arxiv.org/abs/2401.15947
- **BibTeX Key**: `lin2024moellava`

## Abstract
Scaling Multimodal Large Language Models typically inflates computational and serving costs. We introduce MoE-LLaVA, a sparse Mixture-of-Experts framework for efficient multimodal learning. MoE-LLaVA transforms dense feed-forward networks in multimodal LLMs into sparsely activated experts. A learned router dynamically dispatches visual and textual tokens to top-k specialized experts during forward passes. MoE-LLaVA achieves comparable or superior benchmark performance to dense 13B models while activating only 3.6B parameters during inference, cutting computational latency by over 50%.

## Key Extracted Contributions
1. Sparsely activated experts specialize spontaneously in different visual modalities (OCR, fine texture, spatial layout).
2. Routing tokens dynamically prevents interference between distinct cognitive tasks.
3. Top-2 gating achieves optimal Pareto trade-off between specialization and capacity.
