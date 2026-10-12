# Machine Extraction: Inferring and Executing Programs for Visual Reasoning

- **BibTeX Key**: `johnson2024visualreasoningcompositional`
- **Authors**: Justin Johnson, Bharath Hariharan, Laurens van der Maaten, Judy Hoffman, Li Fei-Fei, C. Lawrence Zitnick, Ross Girshick
- **Venue**: ICCV 2017 (2017)
- **arXiv**: [1705.03633](https://arxiv.org/abs/1705.03633)
- **Code**: https://github.com/facebookresearch/clevr-iep
- **Category**: 04_spatial_relational_reasoning
- **Relevance**: 4 / 5 (Foundational Programmatic Prior)

## Abstract
We present an approach for visual reasoning that infers an execution program from a question and executes that program on an image using specialized neural modules. Our modular approach handles complex compositional reasoning with high sample efficiency.

## Key Empirical Findings
1. Programmatic execution guarantees compositionality and interpretability.
2. Spatial relation modules explicitly shift visual attention coordinates across the scene.
3. Outperformed monolithic models by +28% on compositional benchmarks.

## Authors' Stated Conclusions
Explicit coordinate shifting modules are necessary to propagate attention across spatial relations.

## Open Challenges & Future Scope
Modernizing module networks with LLM code generation and foundation vision backbones.

## Architectural Profile
- **Vision**: ResNet-101
- **Projector**: Neural execution modules
- **LLM**: Seq2Seq program generator
- **Tokens**: N/A
