# Paper Review: Unbiased Scene Graph Generation from Biased Training

| Field | Details |
| :--- | :--- |
| **Authors** | Kaihua Tang, Yulei Niu, Jianqiang Huang, Jiaxin Shi, Hanwang Zhang |
| **Institution(s)** | Nanyang Technological University, Alibaba DAMO Academy |
| **Publication Date / Venue** | 2020 / CVPR 2020 |
| **arXiv ID / Link** | [2002.11949](https://arxiv.org/abs/2002.11949) |
| **Code Repository** | [https://github.com/KaihuaTang/Scene-Graph-Benchmark.pytorch](https://github.com/KaihuaTang/Scene-Graph-Benchmark.pytorch) |
| **Category** | Scene Graphs, Graph Neural Networks & Programmatic Reasoning |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
Uses causal total direct effect (TDE) inference to remove spurious reporting bias in scene graph generation, forcing models to predict rare and informative spatial relationships.

---

## 2. Abstract
> "Scene graph generation is heavily biased toward generic, trivial predicates ('on', 'near'). We formulate SGG using causal inference (counterfactual intervention) to remove context bias, enabling unbiased prediction of fine-grained spatial and semantic relationships."

---

## 3. Key Findings
1. Counterfactual causal intervention strips out spurious training set frequency biases.
2. Improves mean Recall (mR@K) by up to 2.5x across informative predicates.
3. Forces the model to look at visual geometric features rather than default frequency counts.

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
Causal counterfactual intervention removes reporting bias and forces models to rely on true visual evidence.

### Future Scope & Unsolved Frontiers
Integration into multimodal LLM decoders.

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `4 / 5` — *Foundational Causal SGG*

### Relevance Rationale
Relevant technique for ensuring that spatial relationship predictions reflect true geometry rather than dataset frequency.

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **Causal TDE Framework**: Total Direct Effect removal of visual and linguistic context bias in SGG.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **Remote Sensing Images**: Tested on Visual Genome natural scenes.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: Causal SGG debiasing.
- **How our inquiry differs**: We apply causal counterfactual thinking to test why text scene graphs fail in VLMs.

---

## 8. Technical Deep-Dive & Architecture Specification

```mermaid
flowchart LR
    A[Visual Input] --> B[Encoder: Faster R-CNN with Causal Heads]
    B --> C[Projector: Bilinear causal effect module]
    C --> D[LLM Backbone: None]
    D --> E[Predictions: N/A]
```

- **Vision Encoder**: `Faster R-CNN with Causal Heads`
- **Cross-Modal Projector**: `Bilinear causal effect module`
- **Language Backbone**: `None`
- **Visual Token Budget**: `N/A`

---

## 9. Actionable Takeaways for Our Codebase & Experiments
- [ ] **Evaluation Standard**: Evaluate spatial models on counterfactual spatial questions (swapping North/South).
