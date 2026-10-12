# Paper Review: Elastic Visual Tokens: Dynamic Token Allocation in MLLMs

| Field | Details |
| :--- | :--- |
| **Authors** | Yabo Sun, Biao Yang, Zhang Li, Xiang Bai |
| **Institution(s)** | Huazhong University of Science and Technology |
| **Publication Date / Venue** | 2025 / CVPR 2025 |
| **arXiv ID / Link** | [2501.06540](https://arxiv.org/abs/2501.06540) |
| **Code Repository** | [https://github.com/Yuliang-Liu/ElasticTokens](https://github.com/Yuliang-Liu/ElasticTokens) |
| **Category** | Token Pruning, Efficient Connectors & Compression |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
Allocates elastic numbers of visual tokens per image crop based on visual complexity, assigning more tokens to dense industrial zones and fewer tokens to rural landscapes.

---

## 2. Abstract
> "Fixed token allocations per crop waste compute on simple regions while starving dense scenes. We introduce Elastic Visual Tokens (EVT), a framework that dynamically scales token budget per crop from 64 to 1,024 tokens based on visual information entropy."

---

## 3. Key Findings
1. Elastic token budgeting achieves +5.3% higher accuracy than uniform budgeting at identical aggregate token cost.
2. Allocates 4x more tokens to dense ports and airfields than agricultural fields.
3. Balances compute across heterogeneous aerial tiles.

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
Visual token allocation should scale with information density rather than physical image area.

### Future Scope & Unsolved Frontiers
Question-conditioned elastic allocation.

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `4 / 5` — *High Architectural Prior*

### Relevance Rationale
Directly relevant for remote sensing where terrain information density varies drastically.

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **Elastic Token Budgeting**: Dynamic token density scaling (64 to 1,024 tokens) based on visual entropy.
- **Compute Rebalancing**: Directs compute to dense urban/port clusters.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **Routing Across Paradigms**: Operates within a single zoom pipeline; does not route to direct overview.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: Adaptive token density within crops.
- **How our inquiry differs**: We integrate elastic token allocation into our overarching multi-paradigm router.

---

## 8. Technical Deep-Dive & Architecture Specification

```mermaid
flowchart LR
    A[Visual Input] --> B[Encoder: SigLIP-SO400M with Elastic Resampler]
    B --> C[Projector: Elastic Resampler]
    C --> D[LLM Backbone: Qwen2-7B]
    D --> E[Predictions: Elastic (64 to 1,024 tokens per tile)]
```

- **Vision Encoder**: `SigLIP-SO400M with Elastic Resampler`
- **Cross-Modal Projector**: `Elastic Resampler`
- **Language Backbone**: `Qwen2-7B`
- **Visual Token Budget**: `Elastic (64 to 1,024 tokens per tile)`

---

## 9. Actionable Takeaways for Our Codebase & Experiments
- [ ] **Tile Budgeting**: Allocate fewer tokens to empty background crops; concentrate tokens on detected clusters.
