# LLaVA-Prune: Accelerating Large Multimodal Models via Token Pruning

- **Authors**: Yuhui Shang, Zhiqiang Zhang, et al.
- **Year**: 2024
- **Venue**: arXiv preprint
- **arXiv**: 2405.08743
- **URL**: https://arxiv.org/abs/2405.08743
- **BibTeX Key**: `shang2024llavaprune`

## Abstract
High-resolution multimodal models suffer from intense compute overhead due to long visual token sequences. We propose LLaVA-Prune, a framework that accelerates LMM inference through instruction-guided token pruning. LLaVA-Prune scores each visual token's relevance to the question tokens at the projector interface and retains only the top-k informative visual tokens. We show that retaining only 40% of visual tokens maintains 98.5% of multimodal benchmark performance while reducing latency by 48%.

## Key Extracted Contributions
1. Instruction-guided scoring at the projector stage reliably identifies task-critical patches.
2. Pruning 60% of tokens reduces decoding time and GPU memory footprint by nearly half.
