# Machine Extraction: XLRS-Bench: Could Your Multimodal LLMs Understand Extremely Large Ultra-High-Resolution Remote Sensing Imagery?

- **BibTeX Key**: `wang2025xlrsbench`
- **Authors**: Fangrun Wang, Haoliang Wang, Zichen Guo, Dong Wang, Yuting Wang, Mengxi Chen, Qiang Ma, Lin Lan, Wen Yang, Jiaming Zhang, Zhiyong Liu, Ming-Ming Sun
- **Venue**: CVPR 2025 (2025)
- **arXiv**: [2503.23771](https://arxiv.org/abs/2503.23771)
- **Code**: https://github.com/WHU-USI/XLRS-Bench
- **Category**: 01_uhr_remote_sensing
- **Relevance**: 5 / 5 (Critical Foundation Benchmark)

## Abstract
Multimodal Large Language Models (MLLMs) have made remarkable strides in natural image comprehension, yet their capability on extremely large ultra-high-resolution (UHR) remote sensing imagery remains largely unmapped. Standard remote sensing images frequently exceed 8000x8000 pixels, where targets occupy only dozens of pixels against massive geospatial backgrounds. In this paper, we introduce XLRS-Bench, the first comprehensive benchmark tailored for UHR remote sensing MLLM evaluation. XLRS-Bench contains 45,942 annotations spanning 16 vision-language tasks covering fine-grained perception, complex relational reasoning, cross-region counting, and multi-temporal change. Extensive evaluations of over 20 proprietary and open-source MLLMs reveal substantial performance degradation caused by excessive downscaling and fragmentation during tiling.

## Key Empirical Findings
1. SOTA models drop significantly below human performance on UHR imagery compared to natural benchmarks.
2. Resizing obliterates sub-100-pixel targets.
3. Independent tiling preserves local details but severs cross-tile context, collapsing relational reasoning.
4. Establishes the 16-task taxonomy including spatial relationships and counting.

## Authors' Stated Conclusions
Fixed token budgets and rigid input resolutions in modern VLMs cannot natively handle gigapixel earth observation imagery. Uniform tiling and downscaling represent opposite, flawed extremes.

## Open Challenges & Future Scope
Requires dynamic multi-scale visual token allocation, spatial relation preservation across tiles, and active zoom mechanisms.

## Architectural Profile
- **Vision**: Evaluates ViT-H/14, InternViT-6B, SigLIP-SO400M across baselines
- **Projector**: MLP / Resampler variants across tested models
- **LLM**: Qwen2.5, Llama-3, GPT-4V, Gemini 1.5 Pro
- **Tokens**: Varies by baseline (576 to 4,096 tokens)
