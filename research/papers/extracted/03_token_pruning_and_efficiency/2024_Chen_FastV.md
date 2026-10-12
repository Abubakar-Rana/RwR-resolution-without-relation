# Machine Extraction: An Image is Worth 1/2 Tokens After Layer 2: Plug-and-Play Sparse Auto-Encoders for Efficient Vision-Language Models (FastV)

- **BibTeX Key**: `chen2024fastv`
- **Authors**: Liang Chen, Haozhe Zhao, Zhiqiang Hu, Jiashuo Sun, Baobao Chang
- **Venue**: ECCV 2024 (2024)
- **arXiv**: [2403.06764](https://arxiv.org/abs/2403.06764)
- **Code**: https://github.com/pkunlp-icler/FastV
- **Category**: 03_token_pruning_and_efficiency
- **Relevance**: 4 / 5 (High Efficiency Prior)

## Abstract
We investigate attention allocation over visual tokens in deep MLLMs and discover that attention over visual tokens dramatically diminishes after the first 2-3 layers. FastV leverages this observation to prune 50-75% of visual tokens after layer 2 in a plug-and-play, training-free manner.

## Key Empirical Findings
1. Visual tokens exhibit extreme attention sparsity in intermediate and late LLM layers.
2. Pruning low-attention tokens after layer 2 retains 99% accuracy on general VQA.
3. Training-free: requires zero fine-tuning.

## Authors' Stated Conclusions
Deep LLM layers primarily perform linguistic reasoning and do not require full visual token resolution.

## Open Challenges & Future Scope
Task-adaptive pruning schedules.

## Architectural Profile
- **Vision**: CLIP ViT-L/14-336
- **Projector**: MLP
- **LLM**: LLaVA-1.5-7B / Vicuna-7B
- **Tokens**: Pruned from 576 to 144 tokens after layer 2
