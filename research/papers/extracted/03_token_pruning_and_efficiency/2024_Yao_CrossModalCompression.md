# Machine Extraction: Cross-Modal Visual Token Compression for Efficient High-Resolution Multimodal Understanding

- **BibTeX Key**: `yao2024crossmodalcompression`
- **Authors**: Yuan Yao, Tianyu Yu, Ao Zhang, Mengdi Li, Haoye Zhang
- **Venue**: EMNLP 2024 (2024)
- **arXiv**: [2407.08711](https://arxiv.org/abs/2407.08711)
- **Code**: https://github.com/THUNLP-MT/CrossModalCompress
- **Category**: 03_token_pruning_and_efficiency
- **Relevance**: 4 / 5 (High Compression Prior)

## Abstract
We propose Cross-Modal Visual Token Compression (CM-VTC). By cross-attending visual patch tokens with the embedded text query, CM-VTC filters out visually salient but task-irrelevant regions, compressing visual sequence length by 70% before the LLM prefill stage.

## Key Empirical Findings
1. Text conditioning before LLM prefill discards 70% of task-irrelevant tokens.
2. Preserves reasoning accuracy across diverse VQA benchmarks.
3. Cross-attention overhead is <15ms.

## Authors' Stated Conclusions
Query-guided pre-LLM compression is vastly more efficient than unconditioned visual downsampling.

## Open Challenges & Future Scope
Multi-turn conversational token caching.

## Architectural Profile
- **Vision**: CLIP ViT-L/14-336
- **Projector**: Cross-Modal Compression Head
- **LLM**: Vicuna-7B
- **Tokens**: Compressed from 576 to 172 tokens
