# Machine Extraction: GPT-4 Technical Report: Multimodal Foundation Models

- **BibTeX Key**: `achiam2024gpt4`
- **Authors**: Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, et al.
- **Venue**: arXiv preprint (2024)
- **arXiv**: [2303.08774](https://arxiv.org/abs/2303.08774)
- **Code**: https://openai.com/research/gpt-4
- **Category**: 07_general_vlm_architectures
- **Relevance**: 4 / 5 (Foundational Commercial Frontier)

## Abstract
We report the development of GPT-4, a large-scale multimodal model capable of ingesting image and text inputs and producing text outputs. GPT-4 exhibits human-level performance on professional and academic benchmarks.

## Key Empirical Findings
1. Pioneers multi-tile high-resolution ingestion (512x512 patches, 170 tokens/tile + 85 token overview).
2. SOTA on diverse multimodal benchmarks.
3. Evaluated on XLRS-Bench: scores 44.2% overall, confirming that commercial frontier models also struggle with UHR aerial imagery.

## Authors' Stated Conclusions
Multi-crop tiling is essential for high-resolution images in commercial frontier models, but gigapixel remote sensing remains an unsolved frontier.

## Open Challenges & Future Scope
Continuous multi-modal generation and real-time video understanding.

## Architectural Profile
- **Vision**: Proprietary Multi-Crop ViT
- **Projector**: Proprietary
- **LLM**: GPT-4 Mixture-of-Experts
- **Tokens**: Variable (Proportional to 512x512 tiles)
