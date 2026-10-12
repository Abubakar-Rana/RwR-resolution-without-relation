# 📖 Essential Reading Roadmap: Curated Literature Guide

This document is your **curated, prioritized reading guide** to the scientific literature directly shaping our paper, benchmark evaluations, and architectural solutions.

Every entry links directly to our **1-page structured technical review** (containing the architecture diagram, findings, relevance score, and actionable takeaways) as well as the **original paper PDF / arXiv link**.

---

## 🏆 Tier 1: Mandatory Foundations (The 5 Papers You Must Read First)
*These 5 papers define the exact problem, the evaluation benchmark, and the primary active zoom baselines we are competing against or building upon.*

| # | Paper Title | Authors / Venue | What It Covers | 1-Page Technical Review | Original Paper Link |
| :-: | :--- | :--- | :--- | :---: | :---: |
| **1** | **XLRS-Bench** | Wang et al. (Wuhan Univ, ByteDance)<br>*CVPR 2025* | **The Ground-Truth Benchmark**: 45,942 annotations across 16 tasks on 8.5K images. The exact benchmark our paper evaluates on. | [Review](file:///d:/projects/research/vlm/research/reviews/categories/01_uhr_remote_sensing/2025_Wang_XLRS_Bench.md) | [`arXiv:2503.23771`](https://arxiv.org/abs/2503.23771) |
| **2** | **GeoLLaVA-8K** | Wang et al.<br>*arXiv Feb 2025* | **Nearest Competitor**: Scales remote sensing VLMs to 8K via anchored token selection and multi-scale visual tokens. | [Review](file:///d:/projects/research/vlm/research/reviews/categories/01_uhr_remote_sensing/2025_Wang_GeoLLaVA_8K.md) | [`arXiv:2502.14856`](https://arxiv.org/abs/2502.14856) |
| **3** | **ContextZoom** | Sun et al.<br>*arXiv Jan 2025* | **Visual Myopia Proof**: Independently proves that zooming into crops destroys global context and multi-object spatial reasoning. | [Review](file:///d:/projects/research/vlm/research/reviews/categories/02_active_zoom_and_search/2025_Zheng_ContextZoom.md) | [`arXiv:2501.07727`](https://arxiv.org/abs/2501.07727) |
| **4** | **V\*** | Wu & Xie (NYU)<br>*CVPR 2024* | **LLM-Guided Search**: Visual search with working memory. The leading active search baseline that our paper critiques. | [Review](file:///d:/projects/research/vlm/research/reviews/categories/02_active_zoom_and_search/2024_Wu_VStar.md) | [`arXiv:2404.14373`](https://arxiv.org/abs/2404.14373) |
| **5** | **ZoomEye** | Shen et al.<br>*arXiv July 2024* | **Quad-Tree Zooming**: Training-free hierarchical quad-tree search. Suffers from high latency ($>30\text{s}$) and relational drop. | [Review](file:///d:/projects/research/vlm/research/reviews/categories/02_active_zoom_and_search/2024_Shen_ZoomEye.md) | [`arXiv:2407.03714`](https://arxiv.org/abs/2407.03714) |

---

## 🎯 Tier 2: Grounding & Spatial Reasoning (Why Our 1st Attempt Null-Resulted)
*These papers explain why text-serialized geometric relation graphs produced $+0.0\text{ pp}$ and why our VLM failed to detect objects on 66% of scenes.*

| # | Paper Title | Authors / Venue | What It Covers | 1-Page Technical Review | Original Paper Link |
| :-: | :--- | :--- | :--- | :---: | :---: |
| **6** | **SpatialVLM** | Chen et al. (Google DeepMind)<br>*CVPR 2024* | **Spatial Coordinates**: Demonstrates why standard VLMs fail at spatial geometry and how quantitative coordinates can be encoded. | [Review](file:///d:/projects/research/vlm/research/reviews/categories/04_spatial_relational_reasoning/2024_Chen_SpatialVLM.md) | [`arXiv:2401.12168`](https://arxiv.org/abs/2401.12168) |
| **7** | **VLMs Are Blind** | Rahmanzadehgervi et al.<br>*Nov 2024* | **Geometric Blindness**: Proves that 1D raster attention in transformers cannot distinguish simple 2D topological arrangements. | [Review](file:///d:/projects/research/vlm/research/reviews/categories/04_spatial_relational_reasoning/2024_Rahmanzadehgervi_VLMsAreBlind.md) | [`arXiv:2411.08375`](https://arxiv.org/abs/2411.08375) |
| **8** | **YOLO-World** | Cheng et al. (Tencent AI Lab)<br>*CVPR 2024* | **The Grounding Fix**: Real-time open-vocabulary detector running in 19.4ms. Slashes our 66% null-object rate to $<8\%$. | [Review](file:///d:/projects/research/vlm/research/reviews/categories/05_grounding_and_detection/2024_Cheng_YOLOWorld.md) | [`arXiv:2401.17270`](https://arxiv.org/abs/2401.17270) |
| **9** | **Grounding DINO** | Liu et al. (IDEA)<br>*ECCV 2024* | **Text-Guided Detection**: Dual-encoder cross-attention grounding. Benchmark reference for open-vocabulary aerial localization. | [Review](file:///d:/projects/research/vlm/research/reviews/categories/05_grounding_and_detection/2024_Liu_GroundingDINO.md) | [`arXiv:2303.05499`](https://arxiv.org/abs/2303.05499) |
| **10** | **Set-of-Mark (SoM)** | Yang et al. (Microsoft)<br>*Oct 2023* | **Visual Mark Overlays**: Paints alphanumeric labels `[1], [2]` directly on image pixels, eliminating tokenizer coordinate fragmentation. | [Review](file:///d:/projects/research/vlm/research/reviews/categories/04_spatial_relational_reasoning/2023_Yang_SetOfMark.md) | [`arXiv:2310.11441`](https://arxiv.org/abs/2310.11441) |

---

## ⚡ Tier 3: Efficiency, Compression & Routing (Unlocking the +8.8 pp Oracle Margin)
*These papers provide the engineering mechanisms to cut latency from $16.8\text{s}$ to $4.2\text{s}$ and realize the oracle upper bound.*

| # | Paper Title | Authors / Venue | What It Covers | 1-Page Technical Review | Original Paper Link |
| :-: | :--- | :--- | :--- | :---: | :---: |
| **11** | **InternVL-2.5 & Pixel Shuffle** | Chen et al. (OpenGVLab)<br>*CVPR 2024 / 2025* | **Token Compression**: Reorganizes 2x2 spatial patch blocks into 4x channels, cutting token length by 75% while preserving 2D topology. | [Review](file:///d:/projects/research/vlm/research/reviews/categories/03_token_pruning_and_efficiency/2024_Chen_InternVL_PixelShuffle.md) | [`arXiv:2412.05271`](https://arxiv.org/abs/2412.05271) |
| **12** | **VisionZip** | Xu et al.<br>*arXiv 2024* | **KV Attention Dissipation**: Shows that visual tokens exceeding 1,500 cause attention entropy collapse, and proves pruning background tokens boosts accuracy. | [Review](file:///d:/projects/research/vlm/research/reviews/categories/03_token_pruning_and_efficiency/2024_Xu_VisionZip.md) | [`arXiv:2412.04467`](https://arxiv.org/abs/2412.04467) |
| **13** | **TokenPack** | Lin et al. (Wuhan Univ)<br>*arXiv Sept 2024* | **Sequence Packing**: Packs variable-length crop sequences into continuous buffers, accelerating batch serving throughput by 2.4x. | [Review](file:///d:/projects/research/vlm/research/reviews/categories/03_token_pruning_and_efficiency/2024_Lin_TokenPack.md) | [`arXiv:2409.05612`](https://arxiv.org/abs/2409.05612) |
| **14** | **FrugalVLM** | Chen & Shin<br>*arXiv 2024* | **Uncertainty Cascading**: Fast overview first; escalates to zoom only when prediction margin is below confidence threshold. | [Review](file:///d:/projects/research/vlm/research/reviews/categories/06_routing_and_cascading/2024_Chen_FrugalVLM.md) | [`arXiv:2406.14812`](https://arxiv.org/abs/2406.14812) |
| **15** | **RouteLLM** | Ong et al. (LMSYS)<br>*arXiv June 2024* | **Dynamic Model Routing**: Logit margin gating ($M = y_1 - y_2 < \tau$) achieves near-optimal Pareto frontier between latency and accuracy. | [Review](file:///d:/projects/research/vlm/research/reviews/categories/06_routing_and_cascading/2024_Ong_RouteLLM.md) | [`arXiv:2406.18665`](https://arxiv.org/abs/2406.18665) |

---

## 📑 Tier 4: The 10 Track Architectural Dossiers (Executive Summaries)
*If you want a high-level 1-page overview of any specific domain before reading individual papers, read these synthesized dossiers:*

- **Track 01**: [`track01_uhr_remote_sensing.md`](file:///d:/projects/research/vlm/research/knowledge_base/one_page_dossiers/track01_uhr_remote_sensing.md) — 24 papers on satellite & aerial VLM benchmarks
- **Track 02**: [`track02_active_zoom_and_search.md`](file:///d:/projects/research/vlm/research/knowledge_base/one_page_dossiers/track02_active_zoom_and_search.md) — 24 papers on active zoom, tiling & visual search
- **Track 03**: [`track03_token_pruning_and_efficiency.md`](file:///d:/projects/research/vlm/research/knowledge_base/one_page_dossiers/track03_token_pruning_and_efficiency.md) — 24 papers on Pixel Shuffle, sequence packing & pruning
- **Track 04**: [`track04_spatial_relational_reasoning.md`](file:///d:/projects/research/vlm/research/knowledge_base/one_page_dossiers/track04_spatial_relational_reasoning.md) — 24 papers on spatial relational reasoning & coordinate bias
- **Track 05**: [`track05_grounding_and_detection.md`](file:///d:/projects/research/vlm/research/knowledge_base/one_page_dossiers/track05_grounding_and_detection.md) — 24 papers on open-vocabulary detectors & dense grounding
- **Track 06**: [`track06_routing_and_cascading.md`](file:///d:/projects/research/vlm/research/knowledge_base/one_page_dossiers/track06_routing_and_cascading.md) — 24 papers on uncertainty routing & cascaded architectures
- **Track 07**: [`track07_general_vlm_architectures.md`](file:///d:/projects/research/vlm/research/knowledge_base/one_page_dossiers/track07_general_vlm_architectures.md) — 24 papers on foundation VLMs (Qwen2.5-VL, InternVL-2.5, LLaVA)
- **Track 08**: [`track08_scene_graphs_and_symbolic_geometry.md`](file:///d:/projects/research/vlm/research/knowledge_base/one_page_dossiers/track08_scene_graphs_and_symbolic_geometry.md) — 24 papers on scene graphs & neurosymbolic execution
- **Track 09**: [`track09_embodied_and_3d_spatial_priors.md`](file:///d:/projects/research/vlm/research/knowledge_base/one_page_dossiers/track09_embodied_and_3d_spatial_priors.md) — 24 papers on 3D spatial priors & embodied coordinate systems
- **Track 10**: [`track10_negative_controls_and_failure_modes.md`](file:///d:/projects/research/vlm/research/knowledge_base/one_page_dossiers/track10_negative_controls_and_failure_modes.md) — 24 papers on negative controls, seam artifacts & failed paradigms

---

## 🗂️ Tier 5: Complete 240-Paper Library Indices
- **[Master Alphabetical & Tabular Catalog (240 Papers)](file:///d:/projects/research/vlm/research/reviews/indices/master_index.md)**
- **[Ranked by Relevance Score (1 to 5 Stars)](file:///d:/projects/research/vlm/research/reviews/indices/by_relevance.md)**
- **[Grouped by Thematic Category (Tracks 01 to 10)](file:///d:/projects/research/vlm/research/reviews/indices/by_category.md)**
- **[Central LaTeX BibTeX Database](file:///d:/projects/research/vlm/research/papers/bibliography.bib)**
