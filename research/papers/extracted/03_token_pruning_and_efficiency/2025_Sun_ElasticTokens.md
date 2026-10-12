# Machine Extraction: Elastic Visual Tokens: Dynamic Token Allocation in MLLMs

- **BibTeX Key**: `sun2025elastictokens`
- **Authors**: Yabo Sun, Biao Yang, Zhang Li, Xiang Bai
- **Venue**: CVPR 2025 (2025)
- **arXiv**: [2501.06540](https://arxiv.org/abs/2501.06540)
- **Code**: https://github.com/Yuliang-Liu/ElasticTokens
- **Category**: 03_token_pruning_and_efficiency
- **Relevance**: 4 / 5 (High Architectural Prior)

## Abstract
Fixed token allocations per crop waste compute on simple regions while starving dense scenes. We introduce Elastic Visual Tokens (EVT), a framework that dynamically scales token budget per crop from 64 to 1,024 tokens based on visual information entropy.

## Key Empirical Findings
1. Elastic token budgeting achieves +5.3% higher accuracy than uniform budgeting at identical aggregate token cost.
2. Allocates 4x more tokens to dense ports and airfields than agricultural fields.
3. Balances compute across heterogeneous aerial tiles.

## Authors' Stated Conclusions
Visual token allocation should scale with information density rather than physical image area.

## Open Challenges & Future Scope
Question-conditioned elastic allocation.

## Architectural Profile
- **Vision**: SigLIP-SO400M with Elastic Resampler
- **Projector**: Elastic Resampler
- **LLM**: Qwen2-7B
- **Tokens**: Elastic (64 to 1,024 tokens per tile)
