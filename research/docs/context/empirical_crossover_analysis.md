# The Empirical Crossover Effect: Detailed Analysis

In ultra-high-resolution vision-language reasoning, the interaction between resolution and reasoning type is non-trivial. This document dissects the **crossover effect** discovered in the RwR experiments.

---

## 1. The Crossover Phenomenon

When moving from whole-image processing (**Direct**) to high-resolution tile inspection (**Selection**):
- **Perceptual (Non-relational) Accuracy**: $+4.1\text{ pp}$ ($95\%$ CI $[+2.4, +5.9]$, $p < 10^{-4}$)
- **Relational (Spatial) Accuracy**: $-4.5\text{ pp}$ ($95\%$ CI $[-7.5, -1.5]$, $p = 0.003$)
- **Net Crossover Interaction**: $-8.6\text{ pp}$ ($95\%$ CI $[-12.1, -5.1]$, permutation $p < 10^{-4}$)

```text
Accuracy (%)
50% ──┐
      │                                   ● Selection (46.7%)
45% ──┼─────────● Direct (42.6%)          │
      │         ▲                         │
40% ──┼─────────┼─────────────────────────┼──────────────
      │         ● Direct (37.9%)          ▼
35% ──┼───────────────────────────────────● Selection (33.4%)
      │                                   [Object Spatial Rel drops to 27.2%]
30% ──┴──────────────────────────────────────────────────
         Non-Relational Tasks                Relational Tasks
```

---

## 2. Per-Task Impact Breakdown

| Task | Category Type | Sample Size ($n$) | Direct Acc (%) | Selection Acc (%) | $\Delta\text{Zoom}$ (pp) | Stat Significance |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Object Colour** | Non-Relational | 800 | 35.4% | 41.4% | **+6.0 pp** | $p < 0.05$ (Holm-corrected) |
| **Regional Land Use** | Non-Relational | 200 | 68.0% | 72.5% | **+4.5 pp** | Positive trend |
| **Object Classification** | Non-Relational | 800 | 35.0% | 37.9% | **+2.9 pp** | Positive trend |
| **Overall Counting** | Non-Relational | 60 | 25.0% | 33.3% | **+8.3 pp** | Positive trend |
| **Route Planning** | Relational | 100 | 40.0% | 41.0% | **+1.0 pp** | Flat |
| **Complex Counting** | Relational | 100 | 56.0% | 51.0% | **-5.0 pp** | Negative trend |
| **Object Spatial Rel.**| Relational | 500 | 32.4% | 27.2% | **-5.2 pp** | Severe degradation |
| **Regional Counting** | Relational | 100 | 45.0% | 39.0% | **-6.0 pp** | Severe degradation |

---

## 3. Why Does Zooming Hurt Spatial Reasoning?

1. **Destruction of Global Topology**:
   When the model receives crops $C_1, C_2, C_3$ alongside an overview, the crops dominate attention because of their high token density. The language model attempts to resolve spatial relations using isolated crops where reference landmarks are cut off.
2. **Crop Boundary Truncation**:
   $22\%$ of parsed detections touch a tile boundary. When an object or its reference entity is bisected by a crop edge, the model fails to register its geometric anchor.
3. **Missing Inter-Crop Spatial Referencing**:
   Standard positional embeddings (like 1D or 2D RoPE) operate within individual crops. Across crops, the model has no innate mechanism to compute Euclidean distances or cardinal vectors without explicit multi-scale positional conditioning.
