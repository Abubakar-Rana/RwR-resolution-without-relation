# Machine Extraction: Eagle: Exploring The Design Space for High-Resolution Multi-Modal LLMs

- **BibTeX Key**: `yue2024eagle`
- **Authors**: Min Shi, Fuxiao Liu, Shihao Wang, Shijia Huang, Sheng Shen, Jiashi Feng, Hengshuang Zhao
- **Venue**: arXiv preprint (2024)
- **arXiv**: [2406.10292](https://arxiv.org/abs/2406.10292)
- **Code**: https://github.com/NVlabs/EAGLE
- **Category**: 02_active_zoom_and_search
- **Relevance**: 4 / 5 (High Architectural Prior)

## Abstract
We present Eagle, an extensive empirical study of high-resolution MLLM architectures. We dissect the trade-offs between tiling strategies, token compression methods, and vision encoder backbones, introducing an optimized vision-centric architecture.

## Key Empirical Findings
1. Multi-scale feature concatenation outperforms single-resolution tiling by +4.3%.
2. Token compression via pixel shuffle preserves spatial relations better than cross-attention resamplers.
3. Establishes Pareto-optimal frontier between visual resolution and token count.

## Authors' Stated Conclusions
Pixel shuffle downsampling preserves 2D spatial locality better than parametric pooling.

## Open Challenges & Future Scope
Active token routing based on query complexity.

## Architectural Profile
- **Vision**: SigLIP-SO400M + Pixel Shuffle
- **Projector**: Pixel Shuffle + MLP
- **LLM**: Vicuna-13B / Llama-3-8B
- **Tokens**: Variable (Proportional to tiles / 4)
