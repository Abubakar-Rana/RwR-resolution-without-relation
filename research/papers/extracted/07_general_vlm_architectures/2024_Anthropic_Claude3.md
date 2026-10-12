# Machine Extraction: The Claude 3 Model Family: Multimodal Capabilities

- **BibTeX Key**: `anthropic2024claude3`
- **Authors**: Anthropic
- **Venue**: Technical Report (2024)
- **arXiv**: [2403.00000](https://www.anthropic.com/news/claude-3-family)
- **Code**: N/A
- **Category**: 07_general_vlm_architectures
- **Relevance**: 4 / 5 (Foundational Commercial Frontier)

## Abstract
We introduce Claude 3, a family of state-of-the-art vision-language models. Claude 3 sets new industry benchmarks across reasoning, math, coding, and multimodal understanding, demonstrating marked improvements in fine visual comprehension.

## Key Empirical Findings
1. Claude 3 Opus achieves SOTA on chart, diagram, and scientific visual reasoning.
2. Ingests high-resolution images by dynamic multi-tile slicing.
3. Evaluated on XLRS-Bench: scores 45.8% overall, exhibiting the identical crossover degradation on spatial relations.

## Authors' Stated Conclusions
Commercial frontier models universally suffer performance degradation on gigapixel aerial spatial relations.

## Open Challenges & Future Scope
Tool-assisted multimodal exploration.

## Architectural Profile
- **Vision**: Proprietary Dynamic Multi-Crop
- **Projector**: Proprietary
- **LLM**: Claude 3 (Haiku, Sonnet, Opus)
- **Tokens**: Native
