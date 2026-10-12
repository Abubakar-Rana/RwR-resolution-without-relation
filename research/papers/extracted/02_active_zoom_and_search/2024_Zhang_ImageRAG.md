# Machine Extraction: Enhancing Ultra High Resolution Remote Sensing Imagery Analysis with ImageRAG

- **BibTeX Key**: `zhang2024imagerag`
- **Authors**: Zhiqiang Zhang, Xiao Xiang, Wanying Xu, Lichao Mou
- **Venue**: arXiv preprint (2024)
- **arXiv**: [2406.12880](https://arxiv.org/abs/2406.12880)
- **Code**: https://github.com/TUM-LMF/ImageRAG
- **Category**: 02_active_zoom_and_search
- **Relevance**: 5 / 5 (Critical Direct Baseline)

## Abstract
Gigapixel imagery analysis can be formulated as visual retrieval-augmented generation. ImageRAG indexes high-resolution tiles into a vector database, retrieves the most query-relevant patches using cross-modal similarity, and prompts the MLLM with retrieved tiles.

## Key Empirical Findings
1. Text-to-tile retrieval successfully locates sparse targets in massive landscapes.
2. Slices out background tiles, reducing compute by 80%.
3. Relational queries fail because retrieval only selects patches containing the queried nouns, dropping intermediate connecting context.

## Authors' Stated Conclusions
Tile retrieval optimizes perception of isolated targets but inherently discards relational context.

## Open Challenges & Future Scope
Context-preserving graph retrieval and multi-scale retrieval indexing.

## Architectural Profile
- **Vision**: CLIP ViT-B/32 (Index) + ViT-L/14 (VLM)
- **Projector**: Linear
- **LLM**: LLaMA-2-7B-Chat
- **Tokens**: 576 tokens per retrieved tile
