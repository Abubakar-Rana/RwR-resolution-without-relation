# Machine Extraction: Benchmarking Spatial and Topological Understanding in MLLMs

- **BibTeX Key**: `zhang2024spatialbench3d`
- **Authors**: Haotian Zhang, Boyuan Chen, Fei Xia
- **Venue**: NeurIPS 2024 (2024)
- **arXiv**: [2406.18910](https://arxiv.org/abs/2406.18910)
- **Code**: https://github.com/google-deepmind/spatial-bench-3d
- **Category**: 04_spatial_relational_reasoning
- **Relevance**: 4 / 5 (High Spatial Prior)

## Abstract
We evaluate topological reasoning in MLLMs, testing graph connectivity, path finding, and topological containment. We show that while models recognize individual nodes and edges, they cannot trace multi-hop connectivity paths across complex visual graphs.

## Key Empirical Findings
1. Models fail on visual path-finding and multi-hop graph connectivity (scores <30%).
2. Topological containment ('is object A inside region B') fails on complex polygons.
3. Confirms that transformer self-attention cannot emulate graph traversal algorithms.

## Authors' Stated Conclusions
Transformer attention cannot natively compute graph traversal and topological connectivity.

## Open Challenges & Future Scope
Hybrid neural-symbolic graph execution.

## Architectural Profile
- **Vision**: Gemini 1.5 Pro, GPT-4V, Claude 3.5
- **Projector**: Native
- **LLM**: Various
- **Tokens**: Native
