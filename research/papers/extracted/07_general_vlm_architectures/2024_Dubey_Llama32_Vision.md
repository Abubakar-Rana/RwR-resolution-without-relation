# Machine Extraction: The Llama 3 Herd of Models: Multimodal Architecture and High-Resolution Adapter

- **BibTeX Key**: `dubey2024llama32vision`
- **Authors**: Abhimanyu Dubey, Jiahui Yu, et al., Llama Team
- **Venue**: arXiv preprint (2024)
- **arXiv**: [2407.21783](https://arxiv.org/abs/2407.21783)
- **Code**: https://github.com/meta-llama/llama-models
- **Category**: 07_general_vlm_architectures
- **Relevance**: 4 / 5 (Foundational Open-Weights VLM)

## Abstract
We present the multimodal extension of Llama 3. By incorporating a vision encoder and cross-attention adapter layers into the Llama 3 backbone, Llama 3.2 Vision achieves competitive multimodal reasoning across image, chart, and document tasks.

## Key Empirical Findings
1. Gated cross-attention adapters preserve text reasoning while injecting visual perception.
2. Supports high-resolution tiling up to 4 tiles.
3. Preserves linguistic reasoning performance with zero regression.

## Authors' Stated Conclusions
Cross-attention adapters provide modular multimodal extension of language models without catastrophic forgetting.

## Open Challenges & Future Scope
Scaling to video and continuous speech.

## Architectural Profile
- **Vision**: ViT-H/14 (Pretrained)
- **Projector**: Cross-Attention Adapter Layers
- **LLM**: Llama-3-8B / Llama-3-70B
- **Tokens**: Variable (up to 4 tiles)
