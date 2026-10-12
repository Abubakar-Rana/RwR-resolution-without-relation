# Machine Extraction: GeoSceneGraph: Remote Sensing Scene Graph Benchmark for Relational VQA

- **BibTeX Key**: `song2024geoscenegraph`
- **Authors**: Kai Song, Fangrun Wang, Haoliang Wang, Wen Yang
- **Venue**: CVPR 2024 (2024)
- **arXiv**: [2404.18900](https://arxiv.org/abs/2404.18900)
- **Code**: https://github.com/WHU-USI/GeoSceneGraph
- **Category**: 08_scene_graphs_and_symbolic_geometry
- **Relevance**: 5 / 5 (Critical Benchmark Prior)

## Abstract
We present GeoSceneGraph, the first large-scale benchmark for scene graph generation and relational VQA in Earth observation. GeoSceneGraph contains 350,000 verified relationships spanning cardinal directions, metric distances, and functional containment across diverse aerial landscapes.

## Key Empirical Findings
1. Modern VLMs score <32% on zero-shot aerial relationship extraction on GeoSceneGraph.
2. Cardinal relationships ('north of', 'southeast of') are the most frequently failed predicate class.
3. Establishing ground-truth scene graphs is essential for diagnosing VLM spatial failures.

## Authors' Stated Conclusions
Remote sensing visual question answering requires dedicated spatial relational scene graph benchmarks.

## Open Challenges & Future Scope
Hierarchical multi-scale scene graph generation.

## Architectural Profile
- **Vision**: Evaluates Faster R-CNN, Motifs, Qwen-VL
- **Projector**: Native
- **LLM**: Various
- **Tokens**: Native
