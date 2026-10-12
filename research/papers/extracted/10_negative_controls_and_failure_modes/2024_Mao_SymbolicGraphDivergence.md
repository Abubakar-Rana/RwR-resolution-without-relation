# Machine Extraction: Symbolic Graph Divergence: Why Tabular and Text Graphs Fail to Guide Neural Attention

- **BibTeX Key**: `mao2024symbolicgraphdivergence`
- **Authors**: Jiayuan Mao, Joshua B. Tenenbaum
- **Venue**: NeurIPS 2024 (2024)
- **arXiv**: [2408.16780](https://arxiv.org/abs/2408.16780)
- **Code**: https://github.com/jiayuanm/graph-divergence
- **Category**: 10_negative_controls_and_failure_modes
- **Relevance**: 5 / 5 (Critical Theoretical Analysis)

## Abstract
We investigate the interface between symbolic graphs and neural attention. We prove that text-serialized graphs diverge mathematically from continuous visual representations: because language models process text tokens sequentially, symbolic graphs cannot modulate 2D spatial attention matrices without dedicated cross-attention adapter layers.

## Key Empirical Findings
1. Text-serialized graphs cannot modulate 2D spatial attention matrices without dedicated architectural adapters.
2. Sequential text reading forces the model to treat graph nodes as linguistic entities rather than spatial coordinates.
3. Confirms that text prompt injection of scene graphs is structurally incapable of guiding visual attention.
4. Concludes that symbolic graphs must be executed by external symbolic interpreters (e.g. Python engines) or injected as visual pixel marks.

## Authors' Stated Conclusions
Text prompts cannot bridge symbolic graphs to neural visual attention; symbolic execution or visual pixel marking is mathematically required.

## Open Challenges & Future Scope
Architectural graph-conditioned attention layers.

## Architectural Profile
- **Vision**: Theoretical Attention Analysis
- **Projector**: N/A
- **LLM**: Transformer self-attention analysis
- **Tokens**: Text tokens vs Visual tokens
