# Machine Extraction: VisionZip: Longer is Not Better for Vision-Language Representation

- **BibTeX Key**: `xu2024visionzip`
- **Authors**: Senqiao Xu, Yicheng Liu, Zhelun Yu, Xila Meng
- **Venue**: arXiv preprint (2024)
- **arXiv**: [2412.04467](https://arxiv.org/abs/2412.04467)
- **Code**: https://github.com/ZJU-FAST/VisionZip
- **Category**: 03_token_pruning_and_efficiency
- **Relevance**: 4 / 5 (High Architectural Prior)

## Abstract
Conventional scaling assumes that more visual tokens unconditionally improve performance. We discover that excessively long visual sequences (e.g. >2,000 tokens) cause attention dissipation in LLM decoders, increasing hallucination rates. VisionZip compresses visual tokens by 75% using redundant patch merging, achieving higher accuracy than uncompressed baselines.

## Key Empirical Findings
1. Token sequences >2,048 tokens induce attention dissipation and prompt dilution in 7B LLMs.
2. Compressing tokens by 75% actually improves reasoning accuracy on complex tasks (+2.8%).
3. Directly refutes the assumption that more visual tokens is always better.

## Authors' Stated Conclusions
Visual token efficiency is not just a speed optimization; compact representations prevent attention dilution in LLMs.

## Open Challenges & Future Scope
Determining optimal token density per modality.

## Architectural Profile
- **Vision**: CLIP ViT-L/14
- **Projector**: VisionZip Token Compressor
- **LLM**: LLaMA-3-8B
- **Tokens**: Compressed from 2,304 to 576 tokens
