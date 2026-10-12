# ZoomEye: Enhancing Multimodal LLMs with Human-like Zooming Capabilities through Tree-based Image Exploration

- **Authors**: Hao Shen, Kun Zhao, Tao Zhao, Ronghui Xu, Zhiqiang Zhang, Mingmin Zhu, Jianwei Yin
- **Year**: 2024
- **Venue**: arXiv preprint
- **arXiv**: 2411.16044
- **URL**: https://arxiv.org/abs/2411.16044
- **BibTeX Key**: `shen2024zoomeye`

## Abstract
Human visual perception naturally employs a hierarchical coarse-to-fine exploration mechanism when interpreting complex visual scenes. In contrast, existing Multimodal Large Language Models (MLLMs) process images at fixed resolutions, failing on micro-evidence. We introduce ZoomEye, a training-free framework that equips any MLLM with human-like zooming capabilities. ZoomEye constructs a dynamic hierarchical image pyramid and uses the MLLM itself to assess region relevance and guide branch-wise exploration. On high-resolution visual question answering benchmarks, ZoomEye improves fine-grained perception by up to 14.2% without requiring any parameter updates.

## Key Extracted Contributions
1. Training-free tree exploration avoids expensive domain fine-tuning.
2. VLM confidence scores provide effective heuristics for pruning unpromising tree branches.
3. Quad-tree tiling causes severe object boundary cuts, requiring overlapping margins.
