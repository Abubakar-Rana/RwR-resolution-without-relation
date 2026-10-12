# Kosmos-2: Grounding Multimodal Large Language Models to the World

- **Authors**: Zhiliang Peng, Wenhui Wang, Li Dong, Yaru Hao, Shaohan Huang, Shuming Ma, Furu Wei
- **Year**: 2024
- **Venue**: ICLR 2024
- **arXiv**: 2306.14824
- **URL**: https://arxiv.org/abs/2306.14824
- **BibTeX Key**: `peng2024kosmos2`

## Abstract
We present Kosmos-2, a Multimodal Large Language Model (MLLM) enabling grounding and referential capabilities. We construct GRIT, a large-scale dataset of grounded image-text pairs containing billions of bounding box links to noun phrases. Kosmos-2 integrates location tokens into its vocabulary and pre-trains on web-scale grounded text. Kosmos-2 excels across grounded visual question answering, referring expression comprehension, and phrase grounding, establishing that grounded pre-training anchors multimodal reasoning firmly in visual reality.

## Key Extracted Contributions
1. Large-scale grounded pre-training anchors language tokens directly to visual patch regions.
2. Interleaving location tokens directly into captions establishes explicit object identity.
3. Significantly reduces hallucination of non-existent objects compared to ungrounded VLMs.
