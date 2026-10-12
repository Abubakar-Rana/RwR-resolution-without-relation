# Machine Extraction: Semantic-Aware Token Compression for Vision-Language Models

- **BibTeX Key**: `huang2024compressvlm`
- **Authors**: Siyuan Huang, Yuhui Shang, Tianhe Ren
- **Venue**: ECCV 2024 (2024)
- **arXiv**: [2408.03450](https://arxiv.org/abs/2408.03450)
- **Code**: https://github.com/THU-Huang/CompressVLM
- **Category**: 03_token_pruning_and_efficiency
- **Relevance**: 3 / 5 (Moderate Efficiency Prior)

## Abstract
We present CompressVLM, an efficient token compression framework for MLLMs. By clustering visual tokens based on feature cosine similarity, CompressVLM compresses background regions into single centroid tokens while preserving target object tokens at full resolution.

## Key Empirical Findings
1. Merges background sky/terrain into single tokens, reducing token count by 65%.
2. Preserves isolated foreground targets without detail degradation.
3. Clustering overhead is <8ms on GPU.

## Authors' Stated Conclusions
Semantic clustering achieves adaptive visual resolution without requiring fixed grids.

## Open Challenges & Future Scope
End-to-end differentiable clustering.

## Architectural Profile
- **Vision**: CLIP ViT-L/14
- **Projector**: Semantic Clustering Projector
- **LLM**: Vicuna-7B
- **Tokens**: Variable (65% reduction)
