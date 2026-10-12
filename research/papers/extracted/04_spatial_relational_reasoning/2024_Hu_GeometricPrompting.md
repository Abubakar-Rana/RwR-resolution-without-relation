# Machine Extraction: Geometric Visual Prompting for Spatial Relation Prediction

- **BibTeX Key**: `hu2024geometricprompting`
- **Authors**: Zhiqiang Hu, Haozhe Zhao, Baobao Chang
- **Venue**: EMNLP 2024 (2024)
- **arXiv**: [2408.11890](https://arxiv.org/abs/2408.11890)
- **Code**: https://github.com/pkunlp-icler/GeoPrompt
- **Category**: 04_spatial_relational_reasoning
- **Relevance**: 4 / 5 (High Prompting Prior)

## Abstract
We introduce Geometric Visual Prompting (GeoPrompt). By drawing directional arrows, connecting lines, and bounding boxes on image canvases, GeoPrompt guides the VLM's visual attention directly along the queried spatial vector, boosting relational accuracy.

## Key Empirical Findings
1. Drawing directional arrows between queried objects improves relational reasoning by +18.4%.
2. Visual arrows guide transformer attention heads along the spatial displacement vector.
3. Works training-free on frozen commercial and open-weights models.

## Authors' Stated Conclusions
Visual geometric prompts (arrows, connecting lines) bridge the spatial reasoning deficit in frozen VLMs.

## Open Challenges & Future Scope
Automated geometric prompt synthesis based on query text.

## Architectural Profile
- **Vision**: GPT-4V / Qwen2-VL with drawn vector arrows
- **Projector**: Native
- **LLM**: Various
- **Tokens**: Native
