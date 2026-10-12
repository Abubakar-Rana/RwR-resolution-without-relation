# Paper Review: SpatialQA: Evaluating 2D and 3D Spatial Knowledge in Large Language Models

| Field | Details |
| :--- | :--- |
| **Authors** | Yuan-Hong Wu, Siyuan Huang, Tianhe Ren |
| **Institution(s)** | Tsinghua University |
| **Publication Date / Venue** | 2024 / ACL 2024 |
| **arXiv ID / Link** | [2405.11890](https://arxiv.org/abs/2405.11890) |
| **Code Repository** | [https://github.com/THU-Wu/SpatialQA](https://github.com/THU-Wu/SpatialQA) |
| **Category** | Spatial & Relational Reasoning in VLMs |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
Evaluates pure language models and multimodal LLMs on spatial topology and mental rotation tasks, showing that language pretraining alone gives models poor spatial intuition.

---

## 2. Abstract
> "We evaluate spatial knowledge in LLMs and MLLMs using SpatialQA, testing coordinate conversion, topological connectivity, and mental rotation. We find that language models possess abstract geographic knowledge but fail completely on geometric spatial reasoning."

---

## 3. Key Findings
1. LLMs know facts (e.g. 'Paris is north of Madrid') but fail on coordinate-based spatial calculation.
2. Multimodal models perform worse than expected when image visual cues contradict common language priors.
3. Spatial mental rotation is near chance in 7B-13B models.

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
Language models cannot perform spatial arithmetic; geometric relationships must be grounded visually or calculated symbolically.

### Future Scope & Unsolved Frontiers
Specialized spatial reasoning pretraining.

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `3 / 5` — *Moderate Spatial Prior*

### Relevance Rationale
Explains why text scene graphs failed: LLMs cannot reliably infer spatial topology from text coordinate lists.

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **Spatial Mental Rotation Evaluation**: Benchmarks spatial rotation and coordinate geometry in LLMs.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **Remote Sensing Images**: Synthetic and indoor benchmark.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: Spatial knowledge evaluation in LLMs.
- **How our inquiry differs**: We focus on solving the visual perception and spatial grounding bottleneck in 8K imagery.

---

## 8. Technical Deep-Dive & Architecture Specification

```mermaid
flowchart LR
    A[Visual Input] --> B[Encoder: Evaluates GPT-4, LLaMA-3, Claude]
    B --> C[Projector: N/A]
    C --> D[LLM Backbone: Various]
    D --> E[Predictions: N/A]
```

- **Vision Encoder**: `Evaluates GPT-4, LLaMA-3, Claude`
- **Cross-Modal Projector**: `N/A`
- **Language Backbone**: `Various`
- **Visual Token Budget**: `N/A`

---

## 9. Actionable Takeaways for Our Codebase & Experiments
- [ ] **Diagnostic Finding**: Do not ask the LLM to calculate geometric distances from coordinate text strings.
