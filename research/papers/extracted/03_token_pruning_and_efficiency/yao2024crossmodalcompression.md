# Cross-Modal Visual Token Compression for Efficient High-Resolution Multimodal Understanding

- **Authors**: Yuan Yao, Ronghao Xu, et al.
- **Year**: 2024
- **Venue**: arXiv preprint
- **arXiv**: 2408.09912
- **URL**: https://arxiv.org/abs/2408.09912
- **BibTeX Key**: `yao2024crossmodalcompression`

## Abstract
Processing ultra-high-resolution inputs with Multimodal Large Language Models is severely limited by quadratic attention overhead. We present Cross-Modal Visual Token Compression (CMVTC), a framework that condenses high-resolution visual token grids under explicit cross-modal textual guidance. CMVTC first identifies task-relevant spatial clusters using cross-attention similarity with query tokens, merges redundant background tokens within clusters, and retains fine-grained tokens for candidate foreground objects. On high-resolution benchmarks, CMVTC achieves 5x token reduction and 3.8x throughput acceleration while maintaining 99.4% of uncompressed accuracy.

## Key Extracted Contributions
1. Combining query-guided token selection with spatial token merging yields superior Pareto efficiency compared to either technique alone.
2. Preserving foreground tokens uncompressed while aggressively merging background tokens preserves fine-grained counting and relational reasoning.
