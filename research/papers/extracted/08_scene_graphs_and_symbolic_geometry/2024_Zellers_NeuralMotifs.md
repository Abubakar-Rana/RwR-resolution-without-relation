# Machine Extraction: Neural Motifs: Scene Graph Parsing with Global Context

- **BibTeX Key**: `zellers2024neuralmotifs`
- **Authors**: Rowan Zellers, Mark Yatskar, Sam Thomson, Yejin Choi
- **Venue**: CVPR 2018 (2018)
- **arXiv**: [1711.06640](https://arxiv.org/abs/1711.06640)
- **Code**: https://github.com/rowanz/neural-motifs
- **Category**: 08_scene_graphs_and_symbolic_geometry
- **Relevance**: 4 / 5 (Foundational SGG Literature)

## Abstract
We analyze visual scene graphs and show that recurring subgraphs ('motifs') dominate empirical datasets. We introduce MotifNet, using bidirectional LSTMs to encode global scene context and decode relationships with strong statistical priors.

## Key Empirical Findings
1. Simple statistical frequency baselines (e.g. $P(relation | subject, object)$) achieve strong performance due to motif biases.
2. Visual detectors often guess relations from object labels rather than true spatial inspection.
3. Warns against benchmark bias in relational reasoning.

## Authors' Stated Conclusions
Scene graph models easily overfit to statistical language correlations rather than visually verifying spatial relations.

## Open Challenges & Future Scope
Unbiased and causal relationship evaluation.

## Architectural Profile
- **Vision**: Faster R-CNN (ResNet-101)
- **Projector**: Bidirectional LSTM Context Encoders
- **LLM**: None
- **Tokens**: N/A
