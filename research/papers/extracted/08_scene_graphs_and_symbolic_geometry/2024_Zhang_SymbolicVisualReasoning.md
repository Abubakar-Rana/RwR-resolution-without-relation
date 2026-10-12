# Machine Extraction: Neuro-Symbolic Visual Reasoning with Dynamic Knowledge Graphs

- **BibTeX Key**: `zhang2024symbolicvisualreasoning`
- **Authors**: Zhiqiang Zhang, Xiao Xiang, Lichao Mou
- **Venue**: IEEE TGRS 2024 (2024)
- **arXiv**: [2407.18910](https://arxiv.org/abs/2407.18910)
- **Code**: https://github.com/TUM-LMF/NeuroSymbolicVLM
- **Category**: 08_scene_graphs_and_symbolic_geometry
- **Relevance**: 4 / 5 (High Symbolic Prior)

## Abstract
We present a neuro-symbolic framework for aerial VQA. Neural models extract visual primitives, which instantiate dynamic spatial knowledge graphs. A symbolic inference engine evaluates spatial rules and constraints to answer geometric and topological questions with zero hallucination.

## Key Empirical Findings
1. Symbolic graph solvers guarantee 100% adherence to geometric constraints.
2. Eliminates cardinal direction and distance hallucinations.
3. Outperforms pure end-to-end neural models by +18.2% on aerial spatial queries.

## Authors' Stated Conclusions
Neuro-symbolic separation delivers mathematically rigorous spatial reasoning that pure neural models cannot achieve.

## Open Challenges & Future Scope
Handling perception uncertainty within symbolic solvers.

## Architectural Profile
- **Vision**: YOLOv8 + Grounding DINO
- **Projector**: Symbolic Graph Builder
- **LLM**: Python Symbolic Engine
- **Tokens**: N/A
