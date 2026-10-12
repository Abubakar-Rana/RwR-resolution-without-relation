# Machine Extraction: ChatEarth: Interactive Geospatial Analysis with Multimodal Large Language Models

- **BibTeX Key**: `li2024chatearth`
- **Authors**: Zhenshi Li, Diliyaer Muhtar, Xueliang Lu
- **Venue**: arXiv preprint (2024)
- **arXiv**: [2406.12876](https://arxiv.org/abs/2406.12876)
- **Code**: https://github.com/NJU-LHRS/ChatEarth
- **Category**: 01_uhr_remote_sensing
- **Relevance**: 3 / 5 (Moderate Prior)

## Abstract
We present ChatEarth, a framework coupling multimodal LLMs with GIS tool execution. By translating natural language instructions into geospatial API calls (e.g., GeoPandas, GDAL), ChatEarth performs complex multi-temporal and spatial operations.

## Key Empirical Findings
1. Programmatic tool calling avoids VLM arithmetic errors in measuring distances and areas.
2. LLMs act as effective semantic planners over GIS functions.

## Authors' Stated Conclusions
Complex geometric calculations should be offloaded to specialized symbolic tools.

## Open Challenges & Future Scope
Unified end-to-end perception and tool invocation.

## Architectural Profile
- **Vision**: CLIP ViT-L
- **Projector**: Linear
- **LLM**: GPT-4 / Qwen-Chat
- **Tokens**: N/A
