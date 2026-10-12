# Machine Extraction: VILA: On Pre-training for Visual Language Models

- **BibTeX Key**: `lin2024vila`
- **Authors**: Ji Lin, Hongxu Yin, Wei Ping, Yao Lu, Pavlo Molchanov, Andrew Tao, Jan Kautz, Mohammad Shoeybi, Song Han
- **Venue**: CVPR 2024 (2024)
- **arXiv**: [2312.07533](https://arxiv.org/abs/2312.07533)
- **Code**: https://github.com/NVlabs/VILA
- **Category**: 07_general_vlm_architectures
- **Relevance**: 4 / 5 (High Architectural Prior)

## Abstract
We present VILA, systematically examining vision-language pretraining recipes. We show that keeping the vision encoder trainable, pretraining on interleaved image-text web data, and multi-image training are foundational for visual reasoning and in-context learning.

## Key Empirical Findings
1. Unfreezing the vision encoder during pretraining improves fine-grained perception (+4.8%).
2. Interleaved image-text pretraining is essential for multi-image and multi-crop spatial reasoning.
3. Preserves language reasoning without degradation.

## Authors' Stated Conclusions
Interleaved pretraining and trainable visual backbones are critical for multi-crop spatial understanding.

## Open Challenges & Future Scope
Video foundation models.

## Architectural Profile
- **Vision**: SigLIP-SO400M (Trainable)
- **Projector**: Two-layer MLP
- **LLM**: Llama-2 / Llama-3 (7B, 13B, 70B)
- **Tokens**: Variable
