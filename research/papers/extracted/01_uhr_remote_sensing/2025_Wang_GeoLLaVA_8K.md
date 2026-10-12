# Machine Extraction: GeoLLaVA-8K: Scaling Remote-Sensing Multimodal Large Language Models to 8K Resolution

- **BibTeX Key**: `wang2025geollava8k`
- **Authors**: Fangrun Wang, Mengxi Chen, Yuting Wang, Dong Wang, Haoliang Wang, Zichen Guo, Zheng Wang, Bo Shan, Lin Lan, Yihua Wang, Heng Wang, Wen Yang, Bo Du, Jiaming Zhang
- **Venue**: arXiv preprint (2025)
- **arXiv**: [2502.14856](https://arxiv.org/abs/2502.14856)
- **Code**: https://github.com/WHU-USI/GeoLLaVA-8K
- **Category**: 01_uhr_remote_sensing
- **Relevance**: 5 / 5 (Critical Direct Comparison)

## Abstract
Processing ultra-high-resolution (UHR) imagery exceeding 8K resolution remains a paramount challenge for remote sensing MLLMs. We present GeoLLaVA-8K, a framework engineered to ingest 8K imagery through hierarchical adaptive patch subdivision, a dual-branch global-local vision aggregator, and high-resolution instruction tuning.

## Key Empirical Findings
1. Dual-branch global-local aggregation retains 85% of fine object features without token blowout.
2. Scales successfully to 8K native resolution.
3. Outperforms standard LLaVA by +14.2% on aerial detection and counting.

## Authors' Stated Conclusions
Dual-scale preservation (low-res global overview + high-res selective patches) is critical for gigapixel remote sensing understanding.

## Open Challenges & Future Scope
Needs dynamic question-guided token routing to cut redundant background tiles in barren terrain.

## Architectural Profile
- **Vision**: CLIP ViT-L/14-336 + Adaptive Patch Slicer
- **Projector**: Two-layer MLP with cross-branch attention
- **LLM**: Vicuna-7B / Llama-3-8B-Instruct
- **Tokens**: 2,880 to 5,760 tokens per image
