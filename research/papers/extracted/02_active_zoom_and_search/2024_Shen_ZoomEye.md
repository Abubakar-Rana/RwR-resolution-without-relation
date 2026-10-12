# Machine Extraction: ZoomEye: Enhancing Multimodal LLMs with Human-like Zooming Capabilities through Tree-based Image Exploration

- **BibTeX Key**: `shen2024zoomeye`
- **Authors**: Hao Shen, Renjie Pi, Jipeng Zhang, Tong Zhang
- **Venue**: EMNLP 2024 (2024)
- **arXiv**: [2406.18217](https://arxiv.org/abs/2406.18217)
- **Code**: https://github.com/ZoomEye-VLM/ZoomEye
- **Category**: 02_active_zoom_and_search
- **Relevance**: 5 / 5 (Critical Direct Comparison)

## Abstract
We present ZoomEye, an exploration framework that models high-resolution image perception as a quad-tree traversal. By evaluating node informativeness, ZoomEye dynamically drills down to fine resolution only in ambiguous regions.

## Key Empirical Findings
1. Quadtree exploration reduces average token processing by 50%.
2. Recursive zoom preserves local details for tiny object queries.
3. Struggles with global questions that require integrating leaf nodes across distinct tree branches.

## Authors' Stated Conclusions
Tree-based zoom excels at local targets but fragments global spatial associations.

## Open Challenges & Future Scope
Cross-branch message passing and global tree summarization.

## Architectural Profile
- **Vision**: CLIP ViT-L/14
- **Projector**: MLP
- **LLM**: Vicuna-7B
- **Tokens**: Variable (576 to 2,304 tokens)
