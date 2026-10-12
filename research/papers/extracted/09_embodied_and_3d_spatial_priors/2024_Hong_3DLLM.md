# Machine Extraction: 3D-LLM: Injecting the 3D World into Large Language Models

- **BibTeX Key**: `hong20243dllm`
- **Authors**: Yining Hong, Haoyu Zhen, Peihao Chen, Shuhong Zheng, Yilun Du, Zhenfang Chen, Chuang Gan
- **Venue**: NeurIPS 2023 (2024)
- **arXiv**: [2307.12981](https://arxiv.org/abs/2307.12981)
- **Code**: https://vis-www.cs.umass.edu/3d-llm/
- **Category**: 09_embodied_and_3d_spatial_priors
- **Relevance**: 4 / 5 (High 3D Multimodal Prior)

## Abstract
We present 3D-LLM, enabling LLMs to understand 3D scenes. By back-projecting 2D multi-view features into 3D voxel representations and aligning them with language, 3D-LLM masters 3D spatial reasoning, dense captioning, and navigation.

## Key Empirical Findings
1. Back-projecting 2D features into 3D coordinates resolves multi-view perspective ambiguities.
2. Preserves physical metric distance and cardinal orientation across the reconstructed scene.
3. Achieves SOTA on ScanQA and 3D referring expression benchmarks.

## Authors' Stated Conclusions
Reconstructing global metric coordinates via 3D back-projection provides spatial representations that multi-view images cannot match.

## Open Challenges & Future Scope
Scaling to city-scale aerial photogrammetry.

## Architectural Profile
- **Vision**: 2D Pre-trained ViT + 3D Feature Extractor
- **Projector**: 3D Perceiver Resampler
- **LLM**: LLaMA-7B / Vicuna-7B
- **Tokens**: 512 3D scene tokens
