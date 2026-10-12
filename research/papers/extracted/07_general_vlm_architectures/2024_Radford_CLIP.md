# Machine Extraction: Learning Transferable Visual Models From Natural Language Supervision

- **BibTeX Key**: `radford2024clip`
- **Authors**: Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, Gretchen Krueger, Ilya Sutskever
- **Venue**: ICML 2021 (2021)
- **arXiv**: [2103.00020](https://arxiv.org/abs/2103.00020)
- **Code**: https://github.com/openai/CLIP
- **Category**: 07_general_vlm_architectures
- **Relevance**: 4 / 5 (Foundational Vision-Language Origin)

## Abstract
We demonstrate that simple pretraining predicting which caption goes with which image achieves competitive zero-shot transfer across 30+ computer vision benchmarks without task-specific training.

## Key Empirical Findings
1. Contrastive language-image pretraining aligns visual features with open-vocabulary text concepts.
2. Enables zero-shot image classification and cross-modal retrieval.
3. Inherent limitation: optimizes for semantic categorization, collapsing fine spatial coordinates.

## Authors' Stated Conclusions
Language supervision produces highly transferable visual concepts, but contrastive loss discards low-level spatial geometry.

## Open Challenges & Future Scope
Dense and localized contrastive learning.

## Architectural Profile
- **Vision**: ResNet-50 / ViT-B/32 / ViT-L/14
- **Projector**: Linear projection to shared metric space
- **LLM**: Transformer text encoder
- **Tokens**: Global pooled embedding
