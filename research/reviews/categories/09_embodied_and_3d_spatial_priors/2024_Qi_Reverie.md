# Paper Review: REVERIE: Remote Embodied Visual Referring Expression in Real Indoor Environments

| Field | Details |
| :--- | :--- |
| **Authors** | Yuankai Qi, Qi Wu, Peter Anderson, Xin Wang, William Yang Wang, Shenghua Gao, Ming-Hsuan Yang |
| **Institution(s)** | University of Adelaide, UCSB, ShanghaiTech |
| **Publication Date / Venue** | 2020 / CVPR 2020 |
| **arXiv ID / Link** | [1904.10151](https://arxiv.org/abs/1904.10151) |
| **Code Repository** | [https://github.com/YuankaiQi/REVERIE](https://github.com/YuankaiQi/REVERIE) |
| **Category** | Embodied AI, 3D Vision-Language & Robot Navigation |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
Establishes the REVERIE benchmark, evaluating embodied agents on locating distant target objects specified by natural language referring expressions across multi-room buildings.

---

## 2. Abstract
> "We introduce REVERIE, a benchmark requiring agents to navigate to a distant room and ground a specific target object described by high-level instructions (e.g. 'bring me the blue mug on the kitchen table')."

---

## 3. Key Findings
1. High-level instructions require joint navigation planning and object grounding.
2. Object grounding success drops severely when the agent stops in sub-optimal viewing positions.
3. Identifies the interplay between viewpoint selection and object recognition.

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
Viewing position and camera angle determine visual grounding success in complex physical spaces.

### Future Scope & Unsolved Frontiers
Active camera repositioning for grounding.

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `3 / 5` — *Moderate Referring Prior*

### Relevance Rationale
Parallels tile crop selection: choosing the right crop bounding box determines whether a small target is recognized.

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **Remote Referring Expression Benchmark**: Combines spatial navigation with fine object grounding.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **Aerial Satellite Imagery**: Indoor Matterport3D dataset.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: Embodied referring expression benchmark.
- **How our inquiry differs**: We operate in overhead gigapixel scenes where viewpoint is fixed but spatial zoom crop must be selected.

---

## 8. Technical Deep-Dive & Architecture Specification

```mermaid
flowchart LR
    A[Visual Input] --> B[Encoder: Faster R-CNN + ResNet-152]
    B --> C[Projector: Cross-modal attention]
    C --> D[LLM Backbone: None (Pre-LLM era)]
    D --> E[Predictions: N/A]
```

- **Vision Encoder**: `Faster R-CNN + ResNet-152`
- **Cross-Modal Projector**: `Cross-modal attention`
- **Language Backbone**: `None (Pre-LLM era)`
- **Visual Token Budget**: `N/A`

---

## 9. Actionable Takeaways for Our Codebase & Experiments
- [ ] **Crop Positioning**: Crop bounding box must be centered on the target to avoid edge clipping.
