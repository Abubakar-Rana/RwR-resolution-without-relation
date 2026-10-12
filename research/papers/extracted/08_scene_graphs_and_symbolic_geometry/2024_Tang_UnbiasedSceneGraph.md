# Machine Extraction: Unbiased Scene Graph Generation from Biased Training

- **BibTeX Key**: `tang2024unbiasedscenegraph`
- **Authors**: Kaihua Tang, Yulei Niu, Jianqiang Huang, Jiaxin Shi, Hanwang Zhang
- **Venue**: CVPR 2020 (2020)
- **arXiv**: [2002.11949](https://arxiv.org/abs/2002.11949)
- **Code**: https://github.com/KaihuaTang/Scene-Graph-Benchmark.pytorch
- **Category**: 08_scene_graphs_and_symbolic_geometry
- **Relevance**: 4 / 5 (Foundational Causal SGG)

## Abstract
Scene graph generation is heavily biased toward generic, trivial predicates ('on', 'near'). We formulate SGG using causal inference (counterfactual intervention) to remove context bias, enabling unbiased prediction of fine-grained spatial and semantic relationships.

## Key Empirical Findings
1. Counterfactual causal intervention strips out spurious training set frequency biases.
2. Improves mean Recall (mR@K) by up to 2.5x across informative predicates.
3. Forces the model to look at visual geometric features rather than default frequency counts.

## Authors' Stated Conclusions
Causal counterfactual intervention removes reporting bias and forces models to rely on true visual evidence.

## Open Challenges & Future Scope
Integration into multimodal LLM decoders.

## Architectural Profile
- **Vision**: Faster R-CNN with Causal Heads
- **Projector**: Bilinear causal effect module
- **LLM**: None
- **Tokens**: N/A
