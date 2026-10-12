# Machine Extraction: Evaluating and Mitigating Visual Hallucinations in Large Multimodal Models

- **BibTeX Key**: `sheng2024visualhallucination`
- **Authors**: Hao Sheng, Siyuan Huang, Tianhe Ren
- **Venue**: CVPR 2024 (2024)
- **arXiv**: [2404.14892](https://arxiv.org/abs/2404.14892)
- **Code**: https://github.com/THU-Sheng/VisualHallucination
- **Category**: 10_negative_controls_and_failure_modes
- **Relevance**: 4 / 5 (Hallucination Diagnostic Prior)

## Abstract
We evaluate object hallucination in MLLMs using the POPE benchmark and introduce a contrastive decoding mitigation. We find that language model priors override visual tokens, causing models to hallucinate co-occurring objects (e.g. hallucinating 'cars' in a parking lot that is empty).

## Key Empirical Findings
1. Language priors override visual tokens whenever visual resolution is ambiguous.
2. Hallucination rate reaches 45% on small objects under low resolution.
3. Contrastive decoding against a blinded vision baseline reduces hallucination.

## Authors' Stated Conclusions
Visual ambiguity directly triggers language model hallucination; grounding in high-resolution visual evidence is mandatory.

## Open Challenges & Future Scope
Grounded decoding verification.

## Architectural Profile
- **Vision**: CLIP ViT-L/14
- **Projector**: MLP
- **LLM**: Vicuna-7B
- **Tokens**: 576 tokens
