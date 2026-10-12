# Flamingo: A Visual Language Model for Few-Shot Learning

- **Authors**: Jean-Baptiste Alayrac, Jeff Donahue, Pauline Luc, Antoine Miech, Iain Barr, Yana Hasson, Karel Lenc, Arthur Mensch, Katie Millican, Malcolm Reynolds, et al.
- **Year**: 2022
- **Venue**: NeurIPS 2022
- **arXiv**: 2206.14045
- **URL**: https://arxiv.org/abs/2206.14045
- **BibTeX Key**: `alayrac2022flamingo`

## Abstract
Building multimodal models capable of rapidly adapting to novel visual tasks with minimal examples is a key milestone in artificial intelligence. We introduce Flamingo, a family of Visual Language Models (VLMs) with state-of-the-art few-shot learning capabilities on open-ended multimodal tasks. Flamingo introduces the Perceiver Resampler, an attention-based architecture that transforms arbitrary numbers of visual feature vectors into a fixed, compact set of visual tokens. Gated cross-attention layers interleaved into pretrained language backbones incorporate these visual tokens without disrupting language priors. Across 16 benchmarks, Flamingo sets new state-of-the-art few-shot performance.

## Key Extracted Contributions
1. Perceiver Resamplers map arbitrarily large input patch grids into a fixed budget (e.g. 64 or 128 tokens) via learned latent queries.
2. Decouples input image resolution from LLM sequence length.
3. Interleaved gated cross-attention preserves language generative capabilities.
