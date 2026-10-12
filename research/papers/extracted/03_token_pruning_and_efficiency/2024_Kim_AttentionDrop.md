# Machine Extraction: Layer-Wise Attention Drop for Fast Vision-Language Inference

- **BibTeX Key**: `kim2024attentiondrop`
- **Authors**: Seungwoo Kim, Jinwoo Shin
- **Venue**: ICML 2024 (2024)
- **arXiv**: [2405.09340](https://arxiv.org/abs/2405.09340)
- **Code**: https://github.com/KAIST-AILab/AttentionDrop
- **Category**: 03_token_pruning_and_efficiency
- **Relevance**: 3 / 5 (Moderate Efficiency Prior)

## Abstract
In deep decoder layers of MLLMs, autoregressive text tokens repeatedly attend to visual tokens with negligible gradient or semantic update. AttentionDrop skips visual cross-attention after layer 16, speeding up token generation by 1.6x.

## Key Empirical Findings
1. Skipping visual attention in deep layers yields 1.6x faster autoregressive decoding.
2. Causes zero degradation on text generation fluency.
3. Slight drop on fine-grained verification tasks.

## Authors' Stated Conclusions
Visual features are primarily absorbed in early and middle layers; deep layers operate predominantly in linguistic space.

## Open Challenges & Future Scope
Dynamic per-token attention skipping.

## Architectural Profile
- **Vision**: CLIP ViT-L/14
- **Projector**: MLP
- **LLM**: Llama-2-7B-Chat
- **Tokens**: 576 tokens (Skipped in layers 16-32)
