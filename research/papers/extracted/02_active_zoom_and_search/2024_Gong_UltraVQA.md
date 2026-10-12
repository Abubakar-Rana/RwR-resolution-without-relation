# Machine Extraction: UltraVQA: Benchmarking and Exploring Active Zoom for Ultra-High-Resolution Images

- **BibTeX Key**: `gong2024ultravqa`
- **Authors**: Yifan Gong, Xingyue Chen, Ziyi Zhang, Xiaodan Liang
- **Venue**: ECCV 2024 (2024)
- **arXiv**: [2407.11430](https://arxiv.org/abs/2407.11430)
- **Code**: https://github.com/GongYifan/UltraVQA
- **Category**: 02_active_zoom_and_search
- **Relevance**: 4 / 5 (High Benchmark Prior)

## Abstract
We present UltraVQA, a benchmark dedicated to ultra-high-resolution visual question answering spanning gigapixel panoramas and aerial scans. We evaluate active zoom agents, dissecting failure modes across isolated target vs multi-object relational questions.

## Key Empirical Findings
1. Active zoom achieves +18.5% on isolated object questions over downsampled baselines.
2. Active zoom drops by -8.2% on multi-object relational questions compared to downsampled baselines.
3. Replicates the crossover effect on independent gigapixel datasets.

## Authors' Stated Conclusions
The resolution-versus-relation tradeoff is a fundamental property of zoom-based perception across all domains.

## Open Challenges & Future Scope
Holistic visual search that retains global relational graphs.

## Architectural Profile
- **Vision**: CLIP ViT-L/14 with Active Zoom
- **Projector**: MLP
- **LLM**: LLaMA-3-8B-Instruct
- **Tokens**: Variable
