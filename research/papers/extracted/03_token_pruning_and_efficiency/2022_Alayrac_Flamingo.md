# Machine Extraction: Flamingo: A Visual Language Model for Few-Shot Learning

- **BibTeX Key**: `alayrac2022flamingo`
- **Authors**: Jean-Baptiste Alayrac, Jeff Donahue, Pauline Luc, Antoine Miech, Iain Barr, Yana Hasson, Karel Lenc, Arthur Mensch, Katie Millican, Malcolm Reynolds, Roman Ring, Eliza Rutherford, Serkan Cabi, Tengda Han, Zhitao Gong, Sina Samangooei, Marianne Monteiro, Jacob Menick, Sebastian Borgeaud, Andrew Brock, Aida Nematzadeh, Sahand Sharifzadeh, Mikolaj Binkowski, Ricardo Barreira, Oriol Vinyals, Andrew Zisserman, Karen Simonyan
- **Venue**: NeurIPS 2022 (2022)
- **arXiv**: [2206.14045](https://arxiv.org/abs/2206.14045)
- **Code**: https://github.com/lucidrains/flamingo-pytorch
- **Category**: 03_token_pruning_and_efficiency
- **Relevance**: 4 / 5 (Foundational Connector Prior)

## Abstract
We present Flamingo, a visual language model that sets a new state of the art in few-shot multimodal learning. Flamingo connects pretrained vision and language models via a Perceiver Resampler that maps variable-sized visual inputs into a fixed number of visual tokens.

## Key Empirical Findings
1. Perceiver Resampler compresses arbitrary visual feature grids into a fixed sequence length (64 tokens).
2. Gated cross-attention preserves language model stability during multi-modal training.
3. Extreme compression (64 tokens) creates an information bottleneck on fine-grained visual details.

## Authors' Stated Conclusions
Fixed-budget resamplers decouple image resolution from LLM sequence length, but risk losing fine spatial details under extreme compression.

## Open Challenges & Future Scope
Dynamic token budgets matching image information content.

## Architectural Profile
- **Vision**: NFNet-F6
- **Projector**: Perceiver Resampler (64 learnable latent queries)
- **LLM**: Chinchilla (70B)
- **Tokens**: Fixed 64 tokens per image
