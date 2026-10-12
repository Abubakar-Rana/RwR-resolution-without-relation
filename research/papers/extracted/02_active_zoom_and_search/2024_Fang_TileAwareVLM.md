# Machine Extraction: Tile-Aware Spatial Encoding for High-Resolution Image Perception

- **BibTeX Key**: `fang2024tileawarevlm`
- **Authors**: Junlin Fang, Siyuan Li, Di Wu
- **Venue**: arXiv preprint (2024)
- **arXiv**: [2408.06712](https://arxiv.org/abs/2408.06712)
- **Code**: https://github.com/ZJU-Fang/TileAwareVLM
- **Category**: 02_active_zoom_and_search
- **Relevance**: 4 / 5 (High Architectural Prior)

## Abstract
When images are sliced into patches, positional embeddings within each patch reset to local coordinates, blinding the model to the patch's global position. We introduce Tile-Aware Spatial Encoding (TASE), which injects global bounding box coordinates directly into patch tokens.

## Key Empirical Findings
1. Local coordinate reset is the primary reason VLMs fail to correlate objects across different tiles.
2. Injecting global bounding box coordinates restores cross-tile cardinal reasoning (+8.9%).
3. Highly effective on synthetic spatial reasoning benchmarks.

## Authors' Stated Conclusions
Explicit global coordinate injection is necessary to restore cross-tile spatial awareness.

## Open Challenges & Future Scope
Testing on complex aerial scenes with 20+ tiles.

## Architectural Profile
- **Vision**: ViT-L/14 with Tile Coordinate Embedding
- **Projector**: MLP with Coordinate Modulation
- **LLM**: Vicuna-7B
- **Tokens**: 1,152 tokens
