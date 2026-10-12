# Machine Extraction: Visual Instruction Tuning

- **BibTeX Key**: `liu2023llava`
- **Authors**: Haotian Liu, Chunyuan Li, Qingyang Wu, Yong Jae Lee
- **Venue**: NeurIPS 2023 (2023)
- **arXiv**: [2304.08485](https://arxiv.org/abs/2304.08485)
- **Code**: https://github.com/haotian-liu/LLaVA
- **Category**: 07_general_vlm_architectures
- **Relevance**: 4 / 5 (Foundational VLM Architecture)

## Abstract
Instruction tuning large language models has shown promising results. We present Visual Instruction Tuning, using machine-generated multimodal instruction-following data to train LLaVA (Large Language and Vision Assistant), connecting vision and language via a simple projection layer.

## Key Empirical Findings
1. Simple linear projection bridges visual features and language tokens surprisingly well.
2. Visual instruction tuning yields strong zero-shot conversational capabilities.
3. Early LLaVA is limited by 224x224 / 336x336 fixed resolution, causing small object blindness.

## Authors' Stated Conclusions
Instruction tuning aligns visual representations with language generation with minimal architectural complexity.

## Open Challenges & Future Scope
High-resolution multi-crop extensions and better projectors.

## Architectural Profile
- **Vision**: CLIP ViT-L/14-224/336
- **Projector**: Linear Projection Layer
- **LLM**: LLaMA-7B / Vicuna-13B
- **Tokens**: 576 tokens
