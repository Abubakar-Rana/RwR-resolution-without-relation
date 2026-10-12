# Machine Extraction: Mind's Eye: Grounded Spatial Reasoning Through Simulation and Scene Graphs

- **BibTeX Key**: `liu2023mindseye`
- **Authors**: Ruibo Liu, Jason Wei, Shixiang Shane Gu, Te-Yen Wu, Soroush Vosoughi, Claire Cui, Denny Zhou, Andrew M. Dai
- **Venue**: ICLR 2023 (2023)
- **arXiv**: [2210.05349](https://arxiv.org/abs/2210.05349)
- **Code**: https://github.com/ruiboliu/minds-eye
- **Category**: 04_spatial_relational_reasoning
- **Relevance**: 4 / 5 (High Symbolic Prior)

## Abstract
Language models struggle with physical and spatial reasoning. We introduce Mind's Eye, which grounds language models by rendering spatial queries into a physical simulation engine (MuJoCo). By inspecting simulation outcomes, the model achieves high zero-shot spatial accuracy.

## Key Empirical Findings
1. Symbolic simulation grounding increases spatial reasoning accuracy by +27.9% over direct LLM prompting.
2. Prevents hallucination of physical contradictions.
3. Converts ambiguous language queries into formal coordinate simulations.

## Authors' Stated Conclusions
Complex spatial and physical reasoning is best solved by offloading to specialized simulation or computational engines.

## Open Challenges & Future Scope
End-to-end integration of visual perception and physics simulation.

## Architectural Profile
- **Vision**: N/A (Symbolic text input)
- **Projector**: N/A
- **LLM**: PaLM-540B / GPT-3
- **Tokens**: N/A
