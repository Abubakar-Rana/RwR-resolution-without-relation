# Shikra: Unleashing Multimodal LLM's Referential Dialogue Magic

- **Authors**: Keqin Chen, Zhao Zhang, Weili Zeng, Richong Zhang, Feng Zhu, Rui Zhao
- **Year**: 2023
- **Venue**: arXiv preprint
- **arXiv**: 2306.15195
- **URL**: https://arxiv.org/abs/2306.15195
- **BibTeX Key**: `chen2023shikra`

## Abstract
Human communication frequently involves referential dialogue, pointing to objects and discussing their attributes. We propose Shikra, a simple and unified multimodal LLM that treats spatial coordinates as standard natural language tokens. Shikra requires no extra positional encoders, coordinate vocabularies, or external detector networks. By reformulating bounding boxes as plain text sequences $[x_1, y_1, x_2, y_2]$, Shikra naturally handles Referring Expression Comprehension (REC), Referring Expression Generation (REG), and grounded visual dialogue with state-of-the-art accuracy.

## Key Extracted Contributions
1. Representing bounding boxes as plain text tokens allows seamless integration into standard language vocabularies.
2. Effective on natural images when objects are large and salient.
3. However, fails on microscopic objects (<32 pixels) where vision tokens lack sufficient spatial resolution.
