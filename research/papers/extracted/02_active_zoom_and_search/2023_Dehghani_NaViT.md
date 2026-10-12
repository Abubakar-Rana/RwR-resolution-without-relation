# Machine Extraction: Patch n' Pack: NaViT, a Vision Transformer for Any Aspect Ratio and Resolution

- **BibTeX Key**: `dehghani2023navit`
- **Authors**: Mostafa Dehghani, Basil Mustafa, Josip Djolonga, Jonathan Heek, Matthias Minderer
- **Venue**: NeurIPS 2023 (2023)
- **arXiv**: [2307.06304](https://arxiv.org/abs/2307.06304)
- **Code**: https://github.com/google-research/scenic
- **Category**: 02_active_zoom_and_search
- **Relevance**: 4 / 5 (Foundational Vision Architecture)

## Abstract
Vision Transformers traditionally mandate rigid square inputs with fixed patch counts. We introduce NaViT (Native Resolution ViT), which enables arbitrary resolution and aspect ratios during training and inference via sequence packing and 2D relative position encodings.

## Key Empirical Findings
1. Eliminates resizing and padding artifacts entirely.
2. Improves training efficiency by 4x via sequence packing.
3. Foundational vision backbone for modern dynamic-resolution VLMs (Qwen2-VL, Gemini).

## Authors' Stated Conclusions
Native resolution processing without padding or fixed aspect ratio is the optimal vision tokenization.

## Open Challenges & Future Scope
Scaling to gigapixel inputs with hierarchical token routing.

## Architectural Profile
- **Vision**: NaViT (Native ViT with 2D-RoPE)
- **Projector**: Linear
- **LLM**: N/A
- **Tokens**: Variable (Proportional to image area)
