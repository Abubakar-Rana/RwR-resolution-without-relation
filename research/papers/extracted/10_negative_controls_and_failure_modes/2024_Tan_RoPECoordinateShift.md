# Machine Extraction: Rotary Position Embedding Shift: The 2D Coordinate Origin Ambiguity in Multi-Tile VLMs

- **BibTeX Key**: `tan2024ropecoordinateshift`
- **Authors**: Sinan Tan, Jinze Bai, Shusheng Yang, Chang Zhou
- **Venue**: NeurIPS 2024 (2024)
- **arXiv**: [2409.18201](https://arxiv.org/abs/2409.18201)
- **Code**: https://github.com/Alibaba-NLP/RoPEShift
- **Category**: 10_negative_controls_and_failure_modes
- **Relevance**: 5 / 5 (Critical Mathematical Analysis)

## Abstract
We analyze 2D Rotary Position Embeddings (2D-RoPE) in multi-crop vision-language models. We reveal a critical structural flaw: because each crop is encoded independently, its 2D-RoPE coordinate frame resets to (0, 0) at the top-left of the crop, blinding the model to relative spatial displacements across crops.

## Key Empirical Findings
1. 2D-RoPE resets to $(0, 0)$ inside each independent crop, creating severe coordinate origin ambiguity.
2. Cross-tile attention cannot compute relative spatial vectors between objects in different crops.
3. Direct mathematical explanation for why Qwen2.5-VL collapses on spatial relationships under tile selection.
4. Proposes continuous global 2D-RoPE offsets.

## Authors' Stated Conclusions
Independent tile cropping breaks 2D-RoPE coordinate consistency, creating local coordinate ambiguity that destroys spatial reasoning.

## Open Challenges & Future Scope
Continuous multi-scale 2D-RoPE.

## Architectural Profile
- **Vision**: NaViT with 2D-RoPE
- **Projector**: Pixel Shuffle
- **LLM**: Qwen2-VL-7B
- **Tokens**: Multi-crop sequences with shifted RoPE
