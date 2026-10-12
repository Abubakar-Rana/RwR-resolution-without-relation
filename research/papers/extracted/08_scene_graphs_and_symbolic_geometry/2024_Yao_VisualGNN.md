# Machine Extraction: Visual Graph Neural Networks for Spatial Relation Prediction

- **BibTeX Key**: `yao2024visualgnn`
- **Authors**: Yuan Yao, Ao Zhang, Mengdi Li, Jiayan Teng
- **Venue**: ECCV 2024 (2024)
- **arXiv**: [2408.05612](https://arxiv.org/abs/2408.05612)
- **Code**: https://github.com/THUNLP-MT/VisualGNN
- **Category**: 08_scene_graphs_and_symbolic_geometry
- **Relevance**: 4 / 5 (High Architectural Prior)

## Abstract
Multimodal LLMs treat visual tokens as flat sequences, ignoring non-local spatial connectivity. VisualGNN introduces a spatial graph neural network into the vision projector, explicitly propagating features along spatial displacement edges before language ingestion.

## Key Empirical Findings
1. Pre-LLM graph message passing improves spatial relation accuracy by +13.2%.
2. Preserves relative spatial vectors between distant visual objects.
3. Adds only 15ms latency to the forward pass.

## Authors' Stated Conclusions
Explicit graph neural message passing in the projector provides the spatial relational inductive bias that flat LLM attention lacks.

## Open Challenges & Future Scope
Dynamic graph topology learning.

## Architectural Profile
- **Vision**: CLIP ViT-L/14 with Spatial GNN
- **Projector**: Spatial Graph Transformer Resampler
- **LLM**: Vicuna-7B
- **Tokens**: 576 tokens
