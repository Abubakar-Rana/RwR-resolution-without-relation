# Project Context: Resolution without Relation (RwR / CTSR)

This document synthesizes the foundational paper of this codebase:  
**"Tile Selection Helps Perception but Hurts Spatial Reasoning in Ultra-High-Resolution Remote Sensing Visual Question Answering"** (`materials/main.pdf`).

---

## 1. Core Motivation & Premise

- **Input Dimension Challenge**: Ultra-High-Resolution (UHR) satellite imagery reaches $8,500 \times 8,500$ pixels or higher.
- **The Classical Dilemma**:
  - *Direct Downscaling*: Compresses the image to fit standard VLM token limits (e.g. $1024 \times 1024$), wiping out small target objects (cars, individual buildings, shipping containers).
  - *Tile Selection / Zooming*: Cuts the scene into high-resolution crops ($1024 \times 1024$ px with $128$ px overlap). Uses a dual saliency + CLIP scoring heuristic to select top-$5$ crops.
- **The Core Hypothesis Tested**:
  When zooming into independent crops, cross-crop spatial relationships are severed. The authors hypothesized that **explicitly reconstructing a cross-tile geometric relation graph** (direction, distance, containment, intersection) and providing it to the VLM in text would restore spatial reasoning.

---

## 2. Pipeline Architecture

```mermaid
flowchart TD
    IMG[UHR Scene: 8,500 x 8,500 px + Question] --> TILE[Tiling: 1024 px with 128 px overlap<br/>~93 tiles/scene]
    IMG --> SAL[Overview Downscaling<br/>Gradient/Variance Saliency]
    TILE --> SCORE[Tile Scoring:<br/>0.35 * Saliency + 0.65 * CLIP(Question, Tile)]
    SCORE --> TOP5[Top-5 Selected Tiles]
    
    TOP5 --> DET[VLM Zero-Shot Extraction<br/>Qwen2.5-VL-7B x 5 calls<br/>Returns JSON boxes in 0-1000]
    DET --> REG[Coordinate Registration<br/>Lift to Global Pixel Frame + Seam Dedup]
    REG --> GRAPH[Geometric Relation Graph<br/>Nearest 6 neighbours per node<br/>Containment, Intersection, Adjacency, Compass]
    
    GRAPH --> FINAL[Final VLM Call: Qwen2.5-VL-7B<br/>Overview + 3 Native Crops + Global Objects + Relations]
    FINAL --> ANS[Multiple-Choice Answer A/B/C/D]
```

---

## 3. Four Matched Comparison Methods

1. **Direct**: 1 call, 0.98 MPix, 1,403 tokens, 3.0s latency. Sends downsampled overview only.
2. **Tiling**: 9.15 calls, 7.83 MPix, 11,810 tokens, 5.0s latency. 8 grid tiles independently answered + text vote.
3. **Selection**: 6.10 calls, 7.53 MPix, 12,006 tokens, 16.8s latency. Overview + 3 crops + registered global object list.
4. **Proposed**: 6.10 calls, 7.53 MPix, 12,455 tokens, 16.9s latency. Exactly identical to Selection plus explicit relation lines in prompt.

---

## 4. Benchmark Results on XLRS-Bench-Lite (2,983 Items)

- **Overall Accuracy**: Selection ($43.1\%$) > Proposed ($42.7\%$) > Direct ($41.3\%$) > Tiling ($37.8\%$).
- **Relational Group (800 items)**: Direct ($37.9\%$) > Tiling ($34.0\%$) > Selection ($33.4\%$) = Proposed ($33.4\%$).
- **Non-Relational Group (2,123 items)**: Selection ($46.7\%$) > Proposed ($46.2\%$) > Direct ($42.6\%$) > Tiling ($39.0\%$).
- **Relation Block Effect**: $\Delta r = +0.0\text{ pp}$ ($95\%$ CI $[-2.1, +2.1]$, McNemar $p = 1.00$).

---

## 5. Key Diagnoses & Failure Mechanisms

1. **66% Empty Relation Graphs**: The frozen 7B VLM returned 0 objects for $66\%$ of scenes. On small-object perception (color, classification), failure rate was $98\% - 100\%$.
2. **Relations as Distractors**: On perception questions, adding relations decreased accuracy by $-4.1\text{ pp}$ when present.
3. **Severe Latency Bottleneck**: Local extraction took 13.0s out of 16.8s total ($77\%$ of compute).
4. **Oracle Upper Bound**: Picking the best of Direct vs Selection per item hits **51.2%** (+8.1 pp).
