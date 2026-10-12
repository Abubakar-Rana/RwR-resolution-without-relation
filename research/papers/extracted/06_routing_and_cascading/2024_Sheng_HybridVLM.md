# Machine Extraction: Hybrid-Resolution VLM Inference with Adaptive Routing

- **BibTeX Key**: `sheng2024hybridvlm`
- **Authors**: Hao Sheng, Kai Zheng, Wen Yang
- **Venue**: IEEE TGRS 2024 (2024)
- **arXiv**: [2409.11890](https://arxiv.org/abs/2409.11890)
- **Code**: https://github.com/WHU-USI/HybridVLM
- **Category**: 06_routing_and_cascading
- **Relevance**: 5 / 5 (Critical Direct Comparison)

## Abstract
We introduce HybridVLM for remote sensing visual question answering. Recognizing that macro-geography and micro-objects require different visual granularities, HybridVLM routes questions through either a global holistic pipeline or an active crop pipeline using a query-type classifier.

## Key Empirical Findings
1. Routing queries by question category boosts overall accuracy by +4.8% over either standalone pipeline.
2. Global pipeline answers spatial and landcover questions in 2.5s.
3. Active crop pipeline answers fine object recognition in 12.0s.
4. Blended runtime is 4.8s per item (60% speedup over pure crop pipeline).

## Authors' Stated Conclusions
Hybrid-resolution routing solves the tension between macro scene layout and micro object perception.

## Open Challenges & Future Scope
End-to-end differentiable routing without rule-based category taxonomies.

## Architectural Profile
- **Vision**: CLIP ViT-L/14 (Global + Crop)
- **Projector**: MLP
- **LLM**: Qwen-VL-Chat
- **Tokens**: Global: 576 / Crop: 2,304 tokens
