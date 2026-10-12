# Paper Review: Adaptive Resolution for Vision-Language Models

| Field | Details |
| :--- | :--- |
| **Authors** | Hao Yuan, Jianfei Gao, Siyuan Li |
| **Institution(s)** | Tsinghua University |
| **Publication Date / Venue** | 2024 / arXiv preprint |
| **arXiv ID / Link** | [2405.18900](https://arxiv.org/abs/2405.18900) |
| **Code Repository** | [https://github.com/YuanHao/AdaptiveRes](https://github.com/YuanHao/AdaptiveRes) |
| **Category** | Dynamic Routing, Multi-Resolution & Cascaded VLM Systems |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
Dynamically selects the input image resolution (from 224x224 to 1024x1024) based on a question classifier trained on query semantic embeddings.

---

## 2. Abstract
> "Different visual tasks require drastically different image resolutions. AdaptiveRes trains a query classifier that predicts the minimum required visual resolution for a given query, dispatching OCR and fine detail queries to high resolution while routing scene classification and spatial queries to low resolution."

---

## 3. Key Findings
1. Text query semantics strongly predict the required visual resolution.
2. Spatial orientation and scene-level queries perform optimally at lower resolutions with broader field of view.
3. Saves 55% FLOPs across VQA benchmarks with zero accuracy loss.

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
Query semantics provide a powerful inductive prior for determining required visual resolution.

### Future Scope & Unsolved Frontiers
Joint resolution and crop region selection.

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `4 / 5` — *High Architectural Prior*

### Relevance Rationale
Directly supports our Task-Prior Router: spatial questions should be routed to low-resolution direct view.

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **Query-Guided Resolution Selection**: Predicts necessary visual resolution directly from query text.
- **Spatial Field of View Finding**: Proves spatial orientation queries perform better at lower resolutions.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **Gigapixel Multi-Crop Systems**: Tested on single-image resizing; not multi-crop tile selection.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: Query-guided resolution selection.
- **How our inquiry differs**: We apply query classification to dispatch between full-scene direct overview and multi-crop tile selection.

---

## 8. Technical Deep-Dive & Architecture Specification

```mermaid
flowchart LR
    A[Visual Input] --> B[Encoder: Dynamic ViT (224 to 1024)]
    B --> C[Projector: MLP]
    C --> D[LLM Backbone: LLaMA-3-8B]
    D --> E[Predictions: Variable (196 to 4,096 tokens)]
```

- **Vision Encoder**: `Dynamic ViT (224 to 1024)`
- **Cross-Modal Projector**: `MLP`
- **Language Backbone**: `LLaMA-3-8B`
- **Visual Token Budget**: `Variable (196 to 4,096 tokens)`

---

## 9. Actionable Takeaways for Our Codebase & Experiments
- [ ] **Routing Policy**: Classify questions by keyword/embedding: route 'direction', 'where', 'count' to direct view.
- [ ] **Scientific Grounding**: Cite AdaptiveRes to explain why broad field of view favors relational reasoning.
