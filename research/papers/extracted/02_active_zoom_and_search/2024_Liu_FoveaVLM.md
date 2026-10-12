# Machine Extraction: Foveated Vision-Language Model for Fine-Grained Object Reasoning

- **BibTeX Key**: `liu2024foveavlm`
- **Authors**: Zheng Liu, Hao Wang, Yali Wang, Limin Wang
- **Venue**: NeurIPS 2024 (2024)
- **arXiv**: [2409.11204](https://arxiv.org/abs/2409.11204)
- **Code**: https://github.com/MCG-NJU/FoveaVLM
- **Category**: 02_active_zoom_and_search
- **Relevance**: 4 / 5 (High Architectural Prior)

## Abstract
Uniform high resolution wastes tokens on periphery backgrounds, while cropping discards the periphery entirely. FoveaVLM introduces foveated tokenization: high-resolution tokens at the queried center with log-polar subsampled periphery tokens.

## Key Empirical Findings
1. Retains 100% of periphery visual topology while allocating 70% of tokens to the foveal focus.
2. Preserves spatial relations between focal target and distant peripheral landmarks.
3. Outperforms pure cropping by +11.2% on spatial relation benchmarks.

## Authors' Stated Conclusions
Foveated visual sampling maintains relational anchors that pure cropping destroys.

## Open Challenges & Future Scope
Multiple simultaneous foveal fixation points.

## Architectural Profile
- **Vision**: ViT-L/14 with Log-Polar Tokenizer
- **Projector**: MLP
- **LLM**: Vicuna-7B
- **Tokens**: 768 tokens
