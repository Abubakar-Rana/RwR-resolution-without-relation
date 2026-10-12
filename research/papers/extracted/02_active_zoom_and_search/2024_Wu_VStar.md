# Machine Extraction: V*: Guided Visual Search as a Core Mechanism in Multimodal LLMs

- **BibTeX Key**: `wu2024vstar`
- **Authors**: Penghao Wu, Saining Xie
- **Venue**: CVPR 2024 (2024)
- **arXiv**: [2312.14135](https://arxiv.org/abs/2312.14135)
- **Code**: https://github.com/p-wu/VStar
- **Category**: 02_active_zoom_and_search
- **Relevance**: 5 / 5 (Foundational Visual Search)

## Abstract
Current MLLMs process images passively at uniform resolution. We propose V*, an active visual search framework that leverages LLM world knowledge to guide a visual searcher in discovering minute, high-resolution details in massive scenes.

## Key Empirical Findings
1. Visual search improves high-resolution fine-grained VQA by +14.7% over passive downsampling.
2. Discovers sub-50-pixel targets effectively.
3. Incurs multi-step inference cost (4-6 rounds of visual crop evaluation).

## Authors' Stated Conclusions
Active search bridges the resolution gap without processing all background pixels.

## Open Challenges & Future Scope
Single-step feed-forward search policies and spatial memory.

## Architectural Profile
- **Vision**: CLIP ViT-L/14 + Crop Extractor
- **Projector**: MLP
- **LLM**: LLaMA-2-13B
- **Tokens**: Variable
