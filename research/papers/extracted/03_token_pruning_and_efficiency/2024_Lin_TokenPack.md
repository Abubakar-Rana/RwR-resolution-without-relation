# Machine Extraction: TokenPack: Efficient Visual Token Packing for Multimodal LLMs

- **BibTeX Key**: `lin2024tokenpack`
- **Authors**: Yuhang Lin, Dong Wang, Zichen Guo
- **Venue**: arXiv preprint (2024)
- **arXiv**: [2409.05612](https://arxiv.org/abs/2409.05612)
- **Code**: https://github.com/WHU-USI/TokenPack
- **Category**: 03_token_pruning_and_efficiency
- **Relevance**: 4 / 5 (High Efficiency Prior)

## Abstract
Processing multi-crop images creates uneven sequence lengths across batches, causing severe padding inefficiency. TokenPack introduces visual token packing, concatenating variable-length crop tokens into a continuous packed sequence with segment-based attention masking.

## Key Empirical Findings
1. Sequence packing increases GPU inference throughput by 2.4x across multi-crop workloads.
2. Eliminates padding token compute entirely.
3. Maintains exact mathematical equivalence to unpacked attention.

## Authors' Stated Conclusions
Sequence packing is mandatory for high-throughput serving of multi-tile vision-language models.

## Open Challenges & Future Scope
Integration into vLLM / SGLang serving engines for VLMs.

## Architectural Profile
- **Vision**: SigLIP-SO400M with Packed Sequences
- **Projector**: MLP
- **LLM**: Qwen2-7B-Instruct
- **Tokens**: Variable packed buffer
