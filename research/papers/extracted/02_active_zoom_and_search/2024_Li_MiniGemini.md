# Machine Extraction: Mini-Gemini: Mining the Potential of Multi-Modality Vision Language Models

- **BibTeX Key**: `li2024minigemini`
- **Authors**: Yanwei Li, Yuechen Zhang, Chengyao Wang, Zhisheng Zhong, Jiaya Jia
- **Venue**: arXiv preprint (2024)
- **arXiv**: [2403.18814](https://arxiv.org/abs/2403.18814)
- **Code**: https://github.com/dvlab-research/MiniGemini
- **Category**: 02_active_zoom_and_search
- **Relevance**: 4 / 5 (High Dual-Scale Prior)

## Abstract
We propose Mini-Gemini to mine the potential of MLLMs without costly large-scale retraining. Mini-Gemini utilizes a dual-path design: a low-resolution branch acts as global visual queries, while high-resolution patches serve as keys and values in cross-attention mining.

## Key Empirical Findings
1. Dual-scale cross-attention preserves global scene structure while injecting fine details.
2. Maintains compact token count (same as low-resolution input) while extracting high-resolution details.
3. Outperforms standard single-resolution baselines across multimodal benchmarks.

## Authors' Stated Conclusions
Separating global spatial queries from high-resolution detail keys prevents token explosion.

## Open Challenges & Future Scope
Dynamic patch selection in the high-resolution branch.

## Architectural Profile
- **Vision**: Dual ViT (Low-res 336x336 + High-res 1536x1536)
- **Projector**: Cross-Attention Resampler
- **LLM**: Gemma-2B / Vicuna-7B
- **Tokens**: Fixed 576 tokens
