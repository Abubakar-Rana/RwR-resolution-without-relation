# Token Merging: Your ViT But Faster

- **Authors**: Daniel Bolya, Cheng-Yang Fu, Xiaoliang Dai, Peizhao Zhang, Christoph Feichtenhofer, Judy Hoffman
- **Year**: 2023
- **Venue**: ICLR 2023
- **arXiv**: 2210.09461
- **URL**: https://arxiv.org/abs/2210.09461
- **BibTeX Key**: `bolya2023tome`

## Abstract
We present Token Merging (ToMe), a simple and effective technique to accelerate existing Vision Transformers without retraining. ToMe employs a bipartite soft matching algorithm that pairs and merges mutually similar visual tokens across transformer blocks. Unlike token pruning methods that discard information permanently, ToMe pools information from redundant background regions into unified tokens. Applied across image classification, video action recognition, and multimodal generation, ToMe achieves a 2x to 3x throughput speedup with negligible accuracy degradation.

## Key Extracted Contributions
1. Merging redundant tokens (via bipartite matching) preserves background information much better than outright dropping tokens.
2. Up to 50% of tokens in vision transformers can be merged with zero retraining.
3. Merging maintains spatial representation energy across the full image grid.
