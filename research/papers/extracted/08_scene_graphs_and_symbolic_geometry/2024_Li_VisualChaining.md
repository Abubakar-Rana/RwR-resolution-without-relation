# Machine Extraction: Visual Chaining: Multi-Hop Relational Reasoning in Complex Imagery

- **BibTeX Key**: `li2024visualchaining`
- **Authors**: Zhenshi Li, Diliyaer Muhtar, Xueliang Lu
- **Venue**: CVPR 2024 (2024)
- **arXiv**: [2405.16780](https://arxiv.org/abs/2405.16780)
- **Code**: https://github.com/NJU-LHRS/VisualChaining
- **Category**: 08_scene_graphs_and_symbolic_geometry
- **Relevance**: 4 / 5 (High Relational Prior)

## Abstract
Multi-hop visual reasoning (e.g., 'What is the color of the car to the right of the building behind the tower?') confuses end-to-end VLMs. Visual Chaining parses the query into a sequence of single-hop sub-queries, iteratively chaining attention from entity to entity.

## Key Empirical Findings
1. Multi-hop spatial queries suffer exponential performance drops in monolithic VLMs.
2. Step-by-step visual chaining decomposes multi-hop queries into reliable single-hop operations.
3. Outperforms direct prompting by +21.4% on multi-hop aerial reasoning.

## Authors' Stated Conclusions
Multi-hop spatial reasoning must be executed sequentially along entity chains rather than processed as a monolithic query.

## Open Challenges & Future Scope
Automated chain generation on complex gigapixel scenes.

## Architectural Profile
- **Vision**: CLIP ViT-L/14
- **Projector**: MLP
- **LLM**: LLaMA-3-8B-Instruct
- **Tokens**: Variable
