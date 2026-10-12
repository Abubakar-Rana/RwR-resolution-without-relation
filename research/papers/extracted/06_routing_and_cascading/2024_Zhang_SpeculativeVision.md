# Machine Extraction: Speculative Vision: Accelerating Vision-Language Models with Draft Visual Tokens

- **BibTeX Key**: `zhang2024speculativevision`
- **Authors**: Zhenghao Zhang, Yuxuan Chen, Siyuan Huang
- **Venue**: NeurIPS 2024 (2024)
- **arXiv**: [2408.06740](https://arxiv.org/abs/2408.06740)
- **Code**: https://github.com/THU-Zhang/SpeculativeVision
- **Category**: 06_routing_and_cascading
- **Relevance**: 4 / 5 (High Efficiency Prior)

## Abstract
We introduce Speculative Vision, adapting speculative decoding to multimodal LLMs. A fast draft model processes a low-resolution thumbnail to generate candidate tokens; the full high-resolution model verifies these tokens in parallel, guaranteeing identical output distribution while accelerating generation by 2.2x.

## Key Empirical Findings
1. Low-resolution visual tokens generate draft text tokens with high acceptance rate (78%).
2. Guarantees exact mathematical equivalence to full high-resolution inference.
3. Accelerates autoregressive generation by 2.2x.

## Authors' Stated Conclusions
Speculative execution with multi-scale visual tokens provides lossless inference acceleration.

## Open Challenges & Future Scope
Speculative visual crop selection.

## Architectural Profile
- **Vision**: Draft: ViT-B (Low-res) / Target: ViT-L with crops
- **Projector**: MLP
- **LLM**: Qwen2-7B-Instruct
- **Tokens**: Draft: 256 / Target: 1,536 tokens
