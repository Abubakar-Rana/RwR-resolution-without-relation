# Machine Extraction: GeoChat: Grounded Large Vision-Language Model for Remote Sensing

- **BibTeX Key**: `kuckreja2024geochat`
- **Authors**: Kartik Kuckreja, Muhammad Sohail Danelljan, Salman Khan, Fahad Shahbaz Khan
- **Venue**: CVPR 2024 (2024)
- **arXiv**: [2311.15826](https://arxiv.org/abs/2311.15826)
- **Code**: https://github.com/mbzuai-oryx/GeoChat
- **Category**: 01_uhr_remote_sensing
- **Relevance**: 4 / 5 (High Domain Prior)

## Abstract
We introduce GeoChat, the first grounded large vision-language model versatile enough to perform regional reasoning, referring expression detection, and standard VQA on remote sensing imagery. GeoChat addresses overhead domain gaps by training on a curated high-resolution remote sensing instruction tuning dataset.

## Key Empirical Findings
1. Natural domain VLMs fail on overhead nadir viewpoints and multi-scale aerial targets.
2. Incorporating region coordinate tokens enables direct bounding box prediction in text output.
3. Achieves SOTA on RSVQA and fine-grained classification.

## Authors' Stated Conclusions
Domain-specific instruction tuning with coordinate grounding is essential for remote sensing.

## Open Challenges & Future Scope
Scaling to gigapixel imagery and handling multi-scale tiling without latency penalty.

## Architectural Profile
- **Vision**: CLIP ViT-L/14-336
- **Projector**: Two-layer MLP
- **LLM**: Vicuna-7B-v1.5
- **Tokens**: 576 tokens
