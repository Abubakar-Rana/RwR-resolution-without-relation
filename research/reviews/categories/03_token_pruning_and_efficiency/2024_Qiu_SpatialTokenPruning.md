# Paper Review: Spatial-Preserving Token Pruning for High-Resolution Transformers

| Field | Details |
| :--- | :--- |
| **Authors** | Yuan Qiu, Siyuan Li, Di Wu |
| **Institution(s)** | Zhejiang University |
| **Publication Date / Venue** | 2024 / arXiv preprint |
| **arXiv ID / Link** | [2407.19201](https://arxiv.org/abs/2407.19201) |
| **Code Repository** | [https://github.com/ZJU-Qiu/SpatialPrune](https://github.com/ZJU-Qiu/SpatialPrune) |
| **Category** | Token Pruning, Efficient Connectors & Compression |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
Ensures that 2D grid structure is preserved during token pruning by enforcing regular spatial grid subsampling rather than unstructured token dropping.

---

## 2. Abstract
> "Unstructured token pruning destroys 2D spatial adjacency, scrambling relative positional encodings. We introduce Spatial-Preserving Token Pruning (SPTP), which constrains token reduction to regular spatial strides (e.g. 2x2 or 3x3 block pooling), preserving intact 2D topology."

---

## 3. Key Findings
1. Unstructured token dropping scrambles 2D RoPE positional encodings, degrading spatial relation tasks.
2. Structured strided pruning maintains intact 2D spatial coordinate frames.
3. Retains 98.5% spatial relational reasoning accuracy under 75% token reduction.

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
Structured spatial pruning is essential to prevent positional encoding breakdown in transformers.

### Future Scope & Unsolved Frontiers
Adaptive striding based on local density.

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `4 / 5` — *High Architectural Prior*

### Relevance Rationale
Directly explains why naive token pruning breaks 2D-RoPE in Qwen2.5-VL and provides the fix.

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **Structured Spatial Pruning**: Enforces 2D block strides during token reduction.
- **RoPE Alignment**: Prevents 2D RoPE coordinate degradation.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **Tile Selection**: Operates inside single images; does not handle multi-tile crop selection.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: Structured pruning analysis; proves RoPE vulnerability to unstructured pruning.
- **How our inquiry differs**: We combine structured spatial pruning (Pixel Shuffle) with our multi-scale tile routing.

---

## 8. Technical Deep-Dive & Architecture Specification

```mermaid
flowchart LR
    A[Visual Input] --> B[Encoder: ViT with 2D-RoPE]
    B --> C[Projector: Strided Block Pooling]
    C --> D[LLM Backbone: Qwen2-7B]
    D --> E[Predictions: Pruned by 4x via strided blocks]
```

- **Vision Encoder**: `ViT with 2D-RoPE`
- **Cross-Modal Projector**: `Strided Block Pooling`
- **Language Backbone**: `Qwen2-7B`
- **Visual Token Budget**: `Pruned by 4x via strided blocks`

---

## 9. Actionable Takeaways for Our Codebase & Experiments
- [ ] **Pruning Rule**: Never use unstructured random or top-k token dropping with 2D-RoPE models.
- [ ] **Structural Choice**: Always use regular spatial block downsampling (Pixel Shuffle) to preserve 2D coordinate grid.
