# Paper Review: Aerial-YOLO: Real-Time Tiny Object Detection in Gigapixel Imagery

| Field | Details |
| :--- | :--- |
| **Authors** | Bo Du, Fangrun Wang, Haoliang Wang, Wen Yang |
| **Institution(s)** | Wuhan University |
| **Publication Date / Venue** | 2025 / CVPR 2025 |
| **arXiv ID / Link** | [2502.16780](https://arxiv.org/abs/2502.16780) |
| **Code Repository** | [https://github.com/WHU-USI/AerialYOLO](https://github.com/WHU-USI/AerialYOLO) |
| **Category** | Object Grounding, Detection & Open-Vocabulary Localization |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
Optimizes YOLO for gigapixel aerial imagery, introducing a P2 high-resolution feature pyramid level and spatial attention head to detect sub-15-pixel vehicles and ships in real time.

---

## 2. Abstract
> "Standard YOLOs downsample images by 32x, destroying features of tiny aerial targets. Aerial-YOLO introduces a dedicated P2 detection head operating at 4x downsampling with high-frequency spatial attention, detecting sub-15-pixel targets in gigapixel imagery at 45 FPS."

---

## 3. Key Findings
1. Adding a P2 (4x downsampling) head boosts tiny object recall by +22.4% on aerial imagery.
2. Detects objects as small as 8x8 pixels reliably.
3. Runs in 22ms per 1024x1024 tile on modern GPUs.

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
Retaining shallow 4x feature pyramid layers is mandatory for detecting sub-20-pixel targets in aerial imagery.

### Future Scope & Unsolved Frontiers
Open-vocabulary classification on P2 feature heads.

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `5 / 5` — *Critical Domain Solution*

### Relevance Rationale
High direct relevance: explains how to configure detection heads for tiny aerial targets in our candidate proposal module.

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **P2 Shallow Detection Head**: Detects sub-15-pixel targets that standard P3-P5 heads miss.
- **Real-Time Aerial Throughput**: 45 FPS on aerial tiles.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **Conversational VLM Reasoning**: Pure detector architecture.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: Specialized tiny object aerial detector.
- **How our inquiry differs**: We use Aerial-YOLO features to feed visual marks into our multimodal reasoning engine.

---

## 8. Technical Deep-Dive & Architecture Specification

```mermaid
flowchart LR
    A[Visual Input] --> B[Encoder: YOLOv8-Aerial with P2 Head]
    B --> C[Projector: Anchor-free head]
    C --> D[LLM Backbone: None]
    D --> E[Predictions: Dense grid]
```

- **Vision Encoder**: `YOLOv8-Aerial with P2 Head`
- **Cross-Modal Projector**: `Anchor-free head`
- **Language Backbone**: `None`
- **Visual Token Budget**: `Dense grid`

---

## 9. Actionable Takeaways for Our Codebase & Experiments
- [ ] **Detector Architecture**: Configure YOLO-World with P2 shallow head for detecting tiny vehicles and ships on XLRS-Bench.
