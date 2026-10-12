# Machine Extraction: DenseConnector: Language-Guided Dense Visual Feature Extraction

- **BibTeX Key**: `wang2024denseconnector`
- **Authors**: Huanjin Wang, Zichen Guo, Dong Wang, Wen Yang
- **Venue**: ECCV 2024 (2024)
- **arXiv**: [2405.13800](https://arxiv.org/abs/2405.13800)
- **Code**: https://github.com/WHU-USI/DenseConnector
- **Category**: 03_token_pruning_and_efficiency
- **Relevance**: 4 / 5 (High Architectural Prior)

## Abstract
Standard vision projectors only extract features from the final vision encoder layer, losing intermediate low-level spatial and texture details. DenseConnector pools features across multiple intermediate ViT layers, fusing dense spatial cues into compact visual tokens.

## Key Empirical Findings
1. Intermediate ViT layers contain richer spatial coordinate information than the semantic final layer.
2. Multi-layer feature pooling improves fine object localization by +8.2%.
3. Keeps token count constant.

## Authors' Stated Conclusions
Tapping intermediate encoder layers recovers low-level spatial geometry discarded by deep semantic abstraction.

## Open Challenges & Future Scope
Dynamic layer selection conditioned on task type.

## Architectural Profile
- **Vision**: SigLIP-SO400M (Layers 8, 16, 24)
- **Projector**: DenseConnector MLP
- **LLM**: Qwen-7B
- **Tokens**: 576 tokens
