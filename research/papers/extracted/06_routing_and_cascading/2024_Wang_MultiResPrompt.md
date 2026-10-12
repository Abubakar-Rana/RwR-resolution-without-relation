# Machine Extraction: Multi-Resolution Prompting for Efficient Vision-Language Inference

- **BibTeX Key**: `wang2024multiresprompt`
- **Authors**: Fangrun Wang, Dong Wang, Zichen Guo, Wen Yang
- **Venue**: arXiv preprint (2024)
- **arXiv**: [2408.12190](https://arxiv.org/abs/2408.12190)
- **Code**: https://github.com/WHU-USI/MultiResPrompt
- **Category**: 06_routing_and_cascading
- **Relevance**: 4 / 5 (High Domain Prior)

## Abstract
We explore Multi-Resolution Prompting (MRP) in remote sensing VQA. By analyzing textual query keywords, MRP automatically selects whether to present the model with a global overview, selective high-resolution crops, or a concatenated multi-scale representation.

## Key Empirical Findings
1. Queries querying 'between', 'relative to', or 'direction' gain +5.8% accuracy when evaluated on low-resolution global overviews.
2. Queries querying 'color', 'type', or 'number' gain +7.2% accuracy when evaluated on high-resolution crops.
3. Validates task-prior routing on aerial VQA.

## Authors' Stated Conclusions
Question syntax contains sufficient predictive signal to route queries between global and local visual representations.

## Open Challenges & Future Scope
Continuous multi-scale feature interpolation.

## Architectural Profile
- **Vision**: CLIP ViT-L/14 (Global vs Crop)
- **Projector**: MLP
- **LLM**: Qwen-VL-Chat
- **Tokens**: Variable
