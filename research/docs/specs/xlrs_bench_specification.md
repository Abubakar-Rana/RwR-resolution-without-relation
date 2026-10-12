# XLRS-Bench Benchmark Specification

This document details the tasks, dataset splits, metric formulations, and evaluation protocols for XLRS-Bench (Ultra-High-Resolution Remote Sensing Benchmark).

---

## 1. Dataset Dimensions & Image Characteristics

- **Image Scale**: Average resolution of $\sim 8,500 \times 8,500$ pixels (ranging up to $15,000 \times 15,000$ pixels).
- **Domains**: Optical satellite imagery, high-altitude aerial reconnaissance, urban infrastructure, rural agricultural landscapes, waterways, natural disaster zones (floods, earthquakes).
- **Benchmark Split**:
  - Full Benchmark: 45,942 annotations across 16 tasks.
  - **XLRS-Bench-Lite**: 3,080 four-option multiple-choice items (random chance baseline = $25.0\%$).
  - **Scored Subset**: 2,983 items (excluding 97 multi-select Overall-Land-Use items).

---

## 2. Task Partitioning: Relational vs. Non-Relational

To properly evaluate multi-scale trade-offs, tasks are strictly partitioned:

### A. Relational Task Group ($n = 800$)
Tasks where correct answers require reasoning over spatial topology, multi-region geometry, or cross-tile object distributions:
1. **Object Spatial Relationship** ($n = 500$): Queries such as *"In the image, the two smaller green greenhouses located towards the upper right are positioned in which direction relative to the larger multi-unit residential area?"*
2. **Regional Counting** ($n = 100$): Counting objects strictly inside a bounded regional landmark (e.g. *"How many houses are there inside the red circle?"*).
3. **Counting with Complex Reasoning** ($n = 100$): Counting items that satisfy composite logical conditions across the full scene.
4. **Route Planning** ($n = 100$): Waypoint navigation and shortest path across infrastructure (e.g., from building with red roof to harbor parking lot).

### B. Non-Relational (Perceptual) Task Group ($n = 2,123$)
Tasks where the question targets localized visual attributes, categories, or broad scene categorization:
1. **Object Colour** ($n = 800$): Color of target within a given bounding box / reference.
2. **Object Classification** ($n = 800$): Fine-grained category of an indicated structure.
3. **Regional Land Use** ($n = 200$): Land-cover type within a marked sub-region.
4. **Anomaly Detection & Interpretation** ($n = 100$): Identifying environmental anomalies, water width, or disturbance.
5. **Environmental Condition** ($n = 100$): Seasonality, weather, or scene atmosphere.
6. **Object Motion State** ($n = 60$): Whether vehicles/vessels are stationary, moored, or underway.
7. **Overall Counting** ($n = 60$): Total count of a salient category across the whole view.
8. **Overall Land Use** ($n = 3$ scorable single-select).

### C. Held-Out Group ($n = 60$)
- **Bi-temporal Counting**: Requires cross-image temporal comparison; held out of single-image relational/non-relational taxonomy but tracked in overall scores.

---

## 3. Evaluation Metrics & Statistical Testing

- **Item Accuracy**:
  $$\text{Accuracy} = \frac{1}{N} \sum_{i=1}^N \mathbb{I}(\hat{y}_i = y_i^*)$$
- **Paired McNemar Exact Test**:
  Evaluates significance of paired differences on identical items between baseline $A$ and method $B$:
  $$p = 2 \sum_{k=b}^{\min(b+c, \dots)} \binom{b+c}{k} 0.5^{b+c}$$
  where $b$ is items where $A$ lost and $B$ won, and $c$ is items where $A$ won and $B$ lost.
- **Paired Bootstrap Confidence Intervals**:
  10,000 bootstrap iterations over paired test items to compute non-parametric $95\%$ CIs.
- **Holm-Bonferroni Correction**:
  Applied across per-task comparisons to guard against family-wise error rate inflation.
