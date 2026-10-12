# Machine Extraction: FrugalVLM: Efficient Processing of High-Resolution Images via Cascaded Vision-Language Models

- **BibTeX Key**: `chen2024frugalvlm`
- **Authors**: Hao Chen, Yubo Zhang, Mengmeng Wang, Shenghao Zhang
- **Venue**: ECCV 2024 (2024)
- **arXiv**: [2407.15230](https://arxiv.org/abs/2407.15230)
- **Code**: https://github.com/ZJU-VIP/FrugalVLM
- **Category**: 06_routing_and_cascading
- **Relevance**: 5 / 5 (Critical Direct Comparison)

## Abstract
Processing every image at high resolution incurs prohibitive compute. FrugalVLM introduces a cascaded inference framework: a fast VLM processes a low-resolution downscaled image first; if predictive uncertainty exceeds a calibrated threshold, the image is passed to a high-resolution multi-crop pipeline.

## Key Empirical Findings
1. Cascaded routing answers 65% of queries accurately at low resolution (saves 65% compute).
2. Logit margin $M = p(y_1) - p(y_2)$ provides a reliable uncertainty metric for triggering escalation.
3. Outperforms monolithic high-resolution processing in aggregate accuracy (+2.1%) while running 2.8x faster.

## Authors' Stated Conclusions
Cascaded routing based on logit margin achieves a superior Pareto frontier than uniform high-resolution processing.

## Open Challenges & Future Scope
Adaptive multi-tier cascades.

## Architectural Profile
- **Vision**: Fast: ViT-B (Low-res) / Slow: ViT-L with Multi-Crop
- **Projector**: MLP
- **LLM**: Vicuna-7B
- **Tokens**: Fast: 576 tokens / Slow: 2,880 tokens
