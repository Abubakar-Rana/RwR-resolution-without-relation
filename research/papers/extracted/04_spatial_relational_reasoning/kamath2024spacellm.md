# SpaceLLM: Spatial Reasoning and Coordinate Grounding for 2D/3D Multimodal LLMs

- **Authors**: Amita Kamath, Jack Hessel, et al.
- **Year**: 2024
- **Venue**: arXiv preprint
- **arXiv**: 2406.18234
- **URL**: https://arxiv.org/abs/2406.18234
- **BibTeX Key**: `kamath2024spacellm`

## Abstract
Spatial reasoning requires Multimodal LLMs to map visual inputs into consistent geometric coordinate frames. We present SpaceLLM, a study on spatial representations and coordinate grounding in MLLMs. We evaluate continuous coordinate regressions vs discrete location tokens and introduce 2D relative position bias layers into the multimodal projector. SpaceLLM achieves state-of-the-art results on spatial relation benchmarks, establishing that continuous spatial biases prevent models from confusing directional orientations.

## Key Extracted Contributions
1. Standard 1D sequence position encodings fail to preserve 2D cardinal geometry (North vs East).
2. 2D relative position biases in cross-attention significantly improve directional reasoning accuracy.
3. Discrete location bins are more stable than raw continuous floating-point regression for LLM generation.
