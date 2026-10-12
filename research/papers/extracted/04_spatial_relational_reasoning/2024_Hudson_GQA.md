# Machine Extraction: GQA: A New Dataset for Real-World Visual Reasoning and Compositional Question Answering

- **BibTeX Key**: `hudson2024gqa`
- **Authors**: Drew A. Hudson, Christopher D. Manning
- **Venue**: CVPR 2019 (2019)
- **arXiv**: [1902.09506](https://arxiv.org/abs/1902.09506)
- **Code**: https://cs.stanford.edu/people/dorothys/gqa/
- **Category**: 04_spatial_relational_reasoning
- **Relevance**: 4 / 5 (Foundational Scene Graph Benchmark)

## Abstract
We introduce GQA, a dataset for real-world visual reasoning and compositional question answering. Grounded in dense scene graphs from Visual Genome, GQA mitigates language bias and provides operational execution graphs for every question.

## Key Empirical Findings
1. Real-world scene graph grounding exposes when models guess answers from language priors.
2. Relational questions require multi-hop traversal over visual scene graphs.
3. Models perform well on object recognition but collapse on multi-hop spatial relations.

## Authors' Stated Conclusions
Multi-hop spatial reasoning requires explicit scene graph grounding to prevent spurious language correlation.

## Open Challenges & Future Scope
Scaling to foundation model architectures.

## Architectural Profile
- **Vision**: Faster R-CNN object features
- **Projector**: Graph attention
- **LLM**: None (Pre-LLM era)
- **Tokens**: N/A
