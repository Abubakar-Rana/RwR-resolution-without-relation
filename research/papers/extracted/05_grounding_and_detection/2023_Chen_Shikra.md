# Machine Extraction: Shikra: Unleashing Multimodal LLM's Referential Dialogue Magic

- **BibTeX Key**: `chen2023shikra`
- **Authors**: Keqin Chen, Zhao Zhang, Weili Zeng, Richong Zhang, Feng Zhu, Rui Zhao
- **Venue**: arXiv preprint (2023)
- **arXiv**: [2306.15195](https://arxiv.org/abs/2306.15195)
- **Code**: https://github.com/shikras/shikra
- **Category**: 05_grounding_and_detection
- **Relevance**: 4 / 5 (High Coordinate Prior)

## Abstract
We present Shikra, a multimodal LLM capable of referential dialogue. Shikra treats spatial coordinates as plain text numerical strings, handling Grounded VQA, Referring Expression Comprehension, and Referring Expression Generation within a unified autoregressive architecture.

## Key Empirical Findings
1. Formatting coordinates as plain text strings $[x_{min}, y_{min}, x_{max}, y_{max}]$ works well on prominent, large objects.
2. However, precision degrades severely on objects smaller than 2% of image area.
3. Autoregressive coordinate generation incurs high latency for multi-object scenes.

## Authors' Stated Conclusions
Plain text coordinates are viable for coarse objects, but suffer high latency and low precision on dense tiny targets.

## Open Challenges & Future Scope
Continuous coordinate tokens and sparse regional decoding.

## Architectural Profile
- **Vision**: CLIP ViT-L/14
- **Projector**: Linear
- **LLM**: Vicuna-7B
- **Tokens**: 576 tokens
