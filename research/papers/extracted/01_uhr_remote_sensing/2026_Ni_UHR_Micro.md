# Machine Extraction: UHR-Micro: Diagnosing and Mitigating the Resolution Illusion in Earth Observation VLMs

- **BibTeX Key**: `ni2026uhrmicro`
- **Authors**: Shuai Ni, Zhenghang Zhang, Xian Sun, Kun Fu
- **Venue**: IEEE TGRS 2026 (2026)
- **arXiv**: [2504.09112](https://arxiv.org/abs/2504.09112)
- **Code**: https://github.com/CAS-AIR/UHR-Micro
- **Category**: 01_uhr_remote_sensing
- **Relevance**: 5 / 5 (Critical Empirical Analysis)

## Abstract
While conventional wisdom dictates that higher resolution uniformly improves visual comprehension, our empirical audit on Earth observation VLMs reveals a striking 'resolution illusion': increasing input resolution through dense cropping systematically impairs macro-spatial relational reasoning. We pinpoint this degradation to coordinate frame fragmentation and inter-patch attention attenuation.

## Key Empirical Findings
1. Fine tiles improve object recognition (+6.2%) but degrade directional reasoning (-5.8%).
2. RoPE positional embeddings lose absolute spatial anchors when images are chopped into independent crops.
3. Proposes continuous coordinate encoding to anchor crops into the global image frame.

## Authors' Stated Conclusions
High-resolution tiling without global coordinate alignment creates severe visual dislocation.

## Open Challenges & Future Scope
Unified continuous coordinate representations and dynamic patch dispatching.

## Architectural Profile
- **Vision**: SigLIP-SO400M with Continuous 2D-RoPE
- **Projector**: Spatial Resampler
- **LLM**: Qwen2-VL-7B
- **Tokens**: 2,048 tokens
