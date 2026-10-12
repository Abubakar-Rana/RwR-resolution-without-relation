# Machine Extraction: Topological Invariance and Graph Constraints in Spatial VQA

- **BibTeX Key**: `kwon2025topologicalvqa`
- **Authors**: Minseok Kwon, Jaemin Cho, Mohit Bansal
- **Venue**: ICLR 2025 (2025)
- **arXiv**: [2410.18201](https://arxiv.org/abs/2410.18201)
- **Code**: https://github.com/unc-nlp/TopoVQA
- **Category**: 04_spatial_relational_reasoning
- **Relevance**: 4 / 5 (High Relational Prior)

## Abstract
We propose TopoVQA, enforcing topological graph constraints during language model decoding. By checking intermediate predictions against a symbolic topological consistency checker, TopoVQA prunes physically impossible spatial configurations.

## Key Empirical Findings
1. Topological decoding constraints eliminate 92% of spatial hallucinations.
2. Enforces transitivity and symmetry by construction.
3. Outperforms unconstrained greedy decoding by +11.2% on spatial reasoning benchmarks.

## Authors' Stated Conclusions
Constrained decoding with symbolic geometry checks prevents spatial hallucination in language models.

## Open Challenges & Future Scope
Integration into speculative decoding engines.

## Architectural Profile
- **Vision**: CLIP ViT-L/14
- **Projector**: MLP
- **LLM**: Llama-3-8B-Instruct with Constrained Decoding
- **Tokens**: 576 tokens
