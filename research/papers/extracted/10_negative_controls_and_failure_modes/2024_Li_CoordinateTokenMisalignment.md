# Machine Extraction: Coordinate Token Misalignment: Why Numbers in Prompts Do Not Translate to Spatial Coordinates

- **BibTeX Key**: `li2024coordinatetokenmisalignment`
- **Authors**: Zhenshi Li, Diliyaer Muhtar, Xueliang Lu
- **Venue**: EMNLP 2024 (2024)
- **arXiv**: [2409.14560](https://arxiv.org/abs/2409.14560)
- **Code**: https://github.com/NJU-LHRS/CoordMisalignment
- **Category**: 10_negative_controls_and_failure_modes
- **Relevance**: 5 / 5 (Critical Empirical Analysis)

## Abstract
A common practice prompts LLMs with numerical coordinates. We investigate tokenizer representations of float coordinates and reveal severe misalignment: tokenizers split floating-point coordinates into erratic subword tokens (e.g. '0', '.', '12', '5'), completely scrambling mathematical magnitude and coordinate geometry.

## Key Empirical Findings
1. BPE tokenizers split float coordinate numbers into inconsistent subword fragments.
2. LLM attention cannot reconstruct continuous 2D Euclidean distances from fragmented subword tokens.
3. Direct mathematical explanation for why serializing coordinate boxes into text prompts fails completely.
4. Recommends visual Set-of-Mark prompts or dedicated continuous coordinate heads.

## Authors' Stated Conclusions
BPE tokenizers fundamentally corrupt continuous numerical coordinates; text coordinate prompting is mathematically flawed.

## Open Challenges & Future Scope
Continuous coordinate tokenizers.

## Architectural Profile
- **Vision**: Evaluates Llama-3, Qwen-2, Mistral tokenizers on coordinates
- **Projector**: N/A
- **LLM**: Various
- **Tokens**: Fragmented BPE subword tokens
