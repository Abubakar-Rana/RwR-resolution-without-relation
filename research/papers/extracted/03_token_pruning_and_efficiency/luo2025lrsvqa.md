# When Large Vision-Language Model Meets Large Remote Sensing Imagery: Coarse-to-Fine Text-Guided Token Pruning

- **Authors**: Jiaqi Luo, Yuting Zhang, Xiangrong Yang, Kang Wu, Qingbo Zhu, Linfang Liang, Jian Chen, Yue Li
- **Year**: 2025
- **Venue**: ICCV 2025
- **arXiv**: 2504.08112
- **URL**: https://arxiv.org/abs/2504.08112
- **BibTeX Key**: `luo2025lrsvqa`

## Abstract
Applying Large Vision-Language Models (LVLMs) to large-scale remote sensing imagery is bottlenecked by the overwhelming computational cost of processing thousands of visual tokens. However, in Earth Observation imagery, vast spatial regions (homogeneous ocean, desert, forest) contain no task-relevant evidence. In this paper, we propose LRS-VQA, a coarse-to-fine text-guided token pruning framework. LRS-VQA introduces a hierarchical semantic pruning mechanism that progressively discards visual tokens showing low attention relevance to the query across intermediate vision encoder and LLM layers. On remote sensing VQA benchmarks, LRS-VQA slashes visual token counts by over 70% and cuts inference latency by 3.2x while matching or exceeding the accuracy of unpruned models.

## Key Extracted Contributions
1. Up to 75% of visual tokens in large remote sensing scenes have near-zero cross-attention weight with user questions.
2. Layer-wise progressive pruning preserves gradient flow and prevents information shock.
3. Text-guided pruning acts as an implicit spatial regularizer, filtering distracting background clutter.
