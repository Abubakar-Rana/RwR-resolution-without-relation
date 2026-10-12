# Speculative Vision: Accelerating Vision-Language Inference with Draft Encoders

- **Authors**: Jiaming Zhang, Haoliang Wang, et al.
- **Year**: 2024
- **Venue**: arXiv preprint
- **arXiv**: 2407.15678
- **URL**: https://arxiv.org/abs/2407.15678
- **BibTeX Key**: `zhang2024speculativevision`

## Abstract
We introduce Speculative Vision, a speculative decoding framework for accelerating multimodal vision-language generation. Speculative Vision pairs a target multimodal model with a fast, compact draft model (operating on lower resolution and smaller vision towers). The draft model speculatively generates multiple candidate answer tokens, which are verified in a single forward pass of the target model. We demonstrate that speculative vision guarantees mathematically identical outputs to the target model while delivering 2.1x to 2.8x speedups across diverse visual reasoning benchmarks.

## Key Extracted Contributions
1. Multimodal draft models achieve high token acceptance rates (>75%) on structured multiple-choice VQA.
2. Mathematically guarantees zero accuracy loss relative to target model greedy decoding.
3. Eliminates the trade-off between latency and output fidelity.
