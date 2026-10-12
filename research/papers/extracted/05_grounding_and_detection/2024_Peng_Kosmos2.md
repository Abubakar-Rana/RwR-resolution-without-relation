# Machine Extraction: Kosmos-2: Grounding Multimodal Large Language Models to the World

- **BibTeX Key**: `peng2024kosmos2`
- **Authors**: Zhiliang Peng, Wenhui Wang, Li Dong, Yaru Hao, Shaohan Huang, Shuming Ma, Furu Wei
- **Venue**: ICLR 2024 (2024)
- **arXiv**: [2306.14824](https://arxiv.org/abs/2306.14824)
- **Code**: https://github.com/microsoft/unilm
- **Category**: 05_grounding_and_detection
- **Relevance**: 4 / 5 (Foundational Grounded VLM)

## Abstract
We present Kosmos-2, a grounded multimodal large language model. Kosmos-2 introduces specialized location tokens into the vocabulary, allowing the model to generate text seamlessly interleaved with grounded spatial bounding boxes.

## Key Empirical Findings
1. Discretizing coordinates into 32x32 bins limits spatial resolution to 3.125% of image width/height.
2. Objects smaller than a grid cell (1/32th of image) cannot be uniquely resolved.
3. Validates that discrete grid tokens are fundamentally incompatible with small aerial targets.

## Authors' Stated Conclusions
Fixed-resolution spatial discretization tokens impose a hard spatial resolution floor that fails on small objects.

## Open Challenges & Future Scope
Continuous or hierarchical coordinate tokenization.

## Architectural Profile
- **Vision**: CLIP ViT-L/14
- **Projector**: Linear
- **LLM**: Magneto Transformer (1.6B)
- **Tokens**: 64 location tokens
