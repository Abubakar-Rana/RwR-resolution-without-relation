# Machine Extraction: HiP-VLM: Hierarchical Patching for High-Resolution Vision-Language

- **BibTeX Key**: `dong2024hipvlm`
- **Authors**: Xiaoyi Dong, Pan Zhang, Yuhang Zang, Yuhang Cao, Dahua Lin
- **Venue**: arXiv preprint (2024)
- **arXiv**: [2405.12999](https://arxiv.org/abs/2405.12999)
- **Code**: https://github.com/OpenGVLab/HiP-VLM
- **Category**: 02_active_zoom_and_search
- **Relevance**: 4 / 5 (High Architectural Prior)

## Abstract
We introduce HiP-VLM, structuring visual tokens into a multi-tiered hierarchy. Macro tokens capture global layout, meso tokens model object clusters, and micro tokens encode local textures, coordinated via hierarchical attention masking.

## Key Empirical Findings
1. Multi-tier hierarchy prevents attention dissipation across large token sequences.
2. Macro-to-micro attention preserves spatial coordinates across zoom levels.
3. Outperforms flat multi-crop models on spatial relational benchmarks.

## Authors' Stated Conclusions
Hierarchical visual abstraction preserves spatial relations better than flat token concatenation.

## Open Challenges & Future Scope
Test-time adaptive hierarchy depth.

## Architectural Profile
- **Vision**: InternViT-6B with Hierarchical Pooling
- **Projector**: Hierarchical Resampler
- **LLM**: InternLM2-7B
- **Tokens**: 1,536 tokens
