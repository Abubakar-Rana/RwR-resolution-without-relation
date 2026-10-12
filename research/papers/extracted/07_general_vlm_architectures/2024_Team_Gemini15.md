# Machine Extraction: Gemini 1.5: Unlocking Multimodal Understanding Across Millions of Tokens

- **BibTeX Key**: `team2024gemini15`
- **Authors**: Gemini Team, Google
- **Venue**: arXiv preprint (2024)
- **arXiv**: [2403.05530](https://arxiv.org/abs/2403.05530)
- **Code**: https://deepmind.google/technologies/gemini/
- **Category**: 07_general_vlm_architectures
- **Relevance**: 4 / 5 (Foundational Long-Context Frontier)

## Abstract
We present Gemini 1.5 Pro, a highly compute-efficient multimodal Mixture-of-Experts model capable of recalling information across context windows exceeding 2 million tokens. Gemini 1.5 Pro achieves near-perfect retrieval on 'needle-in-a-haystack' across text, video, and audio.

## Key Empirical Findings
1. 2M token context enables ingestion of hundreds of full-resolution image crops in a single forward pass.
2. 99%+ recall on multimodal needle-in-a-haystack.
3. However, spatial reasoning on aerial images still degrades due to lack of explicit coordinate grounding.

## Authors' Stated Conclusions
Massive context windows solve the token budget problem, but do not automatically resolve geometric spatial reasoning deficits.

## Open Challenges & Future Scope
Spatially grounded long-context reasoning.

## Architectural Profile
- **Vision**: Native Multi-Scale ViT
- **Projector**: Proprietary
- **LLM**: Gemini 1.5 MoE
- **Tokens**: Up to 2,000,000 tokens
