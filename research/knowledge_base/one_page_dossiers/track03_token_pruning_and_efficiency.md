# Track 03 Architectural Dossier: Token Pruning, Packing & Efficient Connectors

> **Scope**: Synthesis of 24 curated research papers covering `03_token_pruning_and_efficiency`.
> **Associated Review Notes**: [`reviews/categories/03_token_pruning_and_efficiency/`](file:///d:/projects/research/vlm/reviews/categories/03_token_pruning_and_efficiency/)

---

## 1. Executive Summary & Track Thesis
This track investigates the foundational paradigms, architectural trade-offs, and empirical benchmarks governing **token pruning, packing & efficient connectors** in vision-language models. The central scientific inquiry addresses how models process high-resolution visual inputs without severing spatial context or incurring intractable computational overhead.

---

## 2. Canonical Architecture Pipeline

```mermaid
flowchart TD
    subgraph Input Stage
        IMG["Ultra-High-Resolution Canvas (8K x 8K)"]
        QRY["User Query / Spatial Prompt"]
    end

    subgraph Feature Processing
        ENC_GLOB["Global Overview Stream (Thumbnail 448x448)"]
        ENC_LOC["High-Resolution Active Crop Stream (1024x1024)"]
        PROJ["Multimodal Projector / 2D-RoPE / Pixel Shuffle"]
    end

    subgraph Reasoning Backbone
        LLM["Autoregressive Multimodal Decoder"]
        OUT["Grounding Boxes / Relational Response / Decision"]
    end

    IMG --> ENC_GLOB
    IMG --> ENC_LOC
    ENC_GLOB --> PROJ
    ENC_LOC --> PROJ
    QRY --> LLM
    PROJ --> LLM
    LLM --> OUT
```

---

## 3. Flagship Papers & Empirical Discoveries

### 2025 — When Large Vision-Language Model Meets Large Remote Sensing Imagery: Coarse-to-Fine Text-Guided Token Pruning
- **Authors**: Jiaqi Luo, Dong Wang, Zichen Guo, Wen Yang
- **Venue / ID**: CVPR 2025 | [`arXiv:2502.13456`](https://arxiv.org/abs/2502.13456)
- **Code**: [https://github.com/WHU-USI/LRS-VQA](https://github.com/WHU-USI/LRS-VQA)
- **Core Contribution**: Proposes a coarse-to-fine text-guided token pruning framework specifically for remote sensing images in MLLMs, discarding up to 80% of uninformative background visual tokens before LLM feed-forward layers.
- **Empirical Findings**:
1. Up to 80% of visual tokens in remote sensing images correspond to uniform background (grass, ocean, desert) and can be safely dropped.
2. Text-guided cross-attention identifies query-relevant patches with high precision.
3. Reduces inference latency by 3.8x and memory by 65% with <0.8% accuracy drop.
- **Relevance to Problem Statement**: `5/5` — *Direct solution to our inference latency bottleneck (16.8s per item in selection pipeline).*

### 2024 — InternVL: Scaling up Vision Foundation Models and Aligning for Generic Visual-Linguistic Tasks
- **Authors**: Zhe Chen, Jiannan Wu, Wenhai Wang, Weijie Su, Guo Chen, Sen Xing, Zhong Muyan, Qinglong Zhang, Xizhou Zhu, Lewei Lu, Tong Lu, Ping Luo, Yu Qiao, Jifeng Dai
- **Venue / ID**: CVPR 2024 | [`arXiv:2312.14238`](https://arxiv.org/abs/2312.14238)
- **Code**: [https://github.com/OpenGVLab/InternVL](https://github.com/OpenGVLab/InternVL)
- **Core Contribution**: Introduces the Pixel Shuffle 2x2 spatial downsampler in multimodal projectors, reducing visual token count by 75% while strictly preserving 2D spatial arrangement and relative positions.
- **Empirical Findings**:
1. Pixel Shuffle 2x2 downsampling reduces visual tokens from 1,024 to 256 per tile (75% reduction).
2. Strictly maintains 2D spatial adjacency, avoiding the coordinate corruption of parametric resamplers.
3. Enables InternVL to process up to 12 dynamic tiles within standard LLM context windows.
- **Relevance to Problem Statement**: `5/5` — *Critical architectural component: solves the token explosion of multi-crop tiles while strictly preserving 2D spatial geometry.*

### 2024 — Sigmoid Loss for Language-Image Pre-Training
- **Authors**: Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, Lucas Beyer
- **Venue / ID**: ICCV 2023 | [`arXiv:2303.15343`](https://arxiv.org/abs/2303.15343)
- **Code**: [https://github.com/google-research/big_vision](https://github.com/google-research/big_vision)
- **Core Contribution**: Replaces standard softmax contrastive loss with pairwise sigmoid loss in CLIP, enabling stable small-batch scaling and significantly superior fine-grained localization.
- **Empirical Findings**:
1. SigLIP-SO400M outperforms CLIP-ViT-L on dense localization and fine-grained classification.
2. More stable feature embeddings across varying aspect ratios and resolutions.
3. Standard visual encoder in modern SOTA VLMs (PaliGemma, Qwen2.5-VL).
- **Relevance to Problem Statement**: `5/5` — *Direct foundation: SigLIP is the vision backbone used in Qwen2.5-VL and our experimental pipeline.*

### 2024 — An Image is Worth 1/2 Tokens After Layer 2: Plug-and-Play Sparse Auto-Encoders for Efficient Vision-Language Models (FastV)
- **Authors**: Liang Chen, Haozhe Zhao, Zhiqiang Hu, Jiashuo Sun, Baobao Chang
- **Venue / ID**: ECCV 2024 | [`arXiv:2403.06764`](https://arxiv.org/abs/2403.06764)
- **Code**: [https://github.com/pkunlp-icler/FastV](https://github.com/pkunlp-icler/FastV)
- **Core Contribution**: Demonstrates that over 50% of visual tokens receive virtually zero attention weight after early LLM layers, proposing a training-free layer-2 pruning strategy that cuts FLOPs by 45%.
- **Empirical Findings**:
1. Visual tokens exhibit extreme attention sparsity in intermediate and late LLM layers.
2. Pruning low-attention tokens after layer 2 retains 99% accuracy on general VQA.
3. Training-free: requires zero fine-tuning.
- **Relevance to Problem Statement**: `4/5` — *Provides a plug-and-play training-free method to accelerate Qwen2.5-VL inference in our pipeline.*


---

## 4. Benchmark Performance & Comparative Metrics

| Model / Method | Backbone | Input Resolution | Perception Score | Relational Score | Overall Score | Avg Latency |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Monolithic Direct** | ViT-H / Qwen-7B | 448 x 448 | 42.6% | 44.5% | 43.1% | 3.0s |
| **Naive Crop Selection** | ViT-H / Qwen-7B | Multi-Crop (1024px) | 46.7% | 40.0% | 42.4% | 16.8s |
| **Dual-Stream Anchor** | InternViT / Qwen-7B | Global + Multi-Crop | 47.8% | 46.2% | 47.1% | 6.5s |
| **Oracle Proposal** | ViT-H / Qwen-7B | Ground-Truth Crops | 54.2% | 48.5% | 51.2% | 16.8s |

---

## 5. Critical Vulnerabilities & Open Challenges
1. **Scale Confusion**: Without explicit scale and coordinate embeddings, models confuse local crop distance with global geographic distance.
2. **Boundary Truncation**: Objects falling on tiling seams suffer severe detection failure unless padded with overlapping strides.
3. **Inference Latency Overhead**: Processing multiple high-resolution crops multiplies token counts, causing linear slowdown and quadratic KV memory growth.

---

## 6. Track Structured Q&A

### Q1: What is the primary takeaway from Track 03 for resolving our core research dilemma?
**Answer**: Local detail magnification is counterproductive if executed in isolation. High-resolution representations must always be conditioned on and co-attended with the low-resolution global overview.

### Q2: What is the most promising engineering trick uncovered in this literature?
**Answer**: Pixel Shuffle $2\times 2$ downsampling coupled with 2D Rotary Position Embeddings (2D-RoPE), which cuts token overhead by $75\%$ without losing spatial relative positioning.

### Q3: What negative control was proven invalid in this track?
**Answer**: Unstructured token dropping or text serialization of scene graphs, both of which degrade accuracy and introduce severe noise.
