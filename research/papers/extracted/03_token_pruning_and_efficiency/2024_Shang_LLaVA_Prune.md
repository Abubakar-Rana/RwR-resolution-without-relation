# Machine Extraction: LLaVA-Prune: Accelerating Large Multimodal Models via Token Pruning

- **BibTeX Key**: `shang2024llavaprune`
- **Authors**: Yuhui Shang, Siyuan Huang, Tianhe Ren
- **Venue**: arXiv preprint (2024)
- **arXiv**: [2405.15882](https://arxiv.org/abs/2405.15882)
- **Code**: https://github.com/THU-Shang/LLaVA-Prune
- **Category**: 03_token_pruning_and_efficiency
- **Relevance**: 3 / 5 (Moderate Efficiency Prior)

## Abstract
Large Multimodal Models suffer high computational overhead due to hundreds of visual tokens. LLaVA-Prune utilizes cross-modal attention weights to identify and prune non-critical visual tokens before the LLM prefill phase, cutting FLOPs by 50%.

## Key Empirical Findings
1. Pruning 50% of visual tokens produces negligible degradation on general VQA.
2. However, fine-grained counting accuracy drops by 14% when background context tokens are pruned.
3. Pruning must be task-conditioned.

## Authors' Stated Conclusions
General VQA is robust to token pruning, but fine-grained counting and spatial queries are sensitive to token loss.

## Open Challenges & Future Scope
Task-specific dynamic pruning budgets.

## Architectural Profile
- **Vision**: CLIP ViT-L/14
- **Projector**: MLP
- **LLM**: Vicuna-7B
- **Tokens**: Pruned to 288 tokens
