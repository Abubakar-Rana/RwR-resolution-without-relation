# Research Problem Statement & Investigation Protocol

> **Project Code**: RwR / CTSR (Resolution without Relation / Cross-Tile Spatial Reasoning)  
> **Target Benchmark**: XLRS-Bench (Ultra-High-Resolution Remote Sensing VQA, ~8,500 × 8,500 px)  
> **Foundation Model**: Qwen2.5-VL-7B-Instruct  
> **Last Updated**: 2026-10-07  
> **Status**: Active Research & Algorithmic Redesign  

---

## 1. Executive Summary & Ground-Truth Experimental Findings

Ultra-high-resolution (UHR) remote sensing scenes pose an extreme multi-scale dilemma for Vision-Language Models (VLMs). Because satellite scenes typically span $8,500 \times 8,500$ pixels or larger, critical objects (vehicles, buildings, river junctions, small infrastructure) often cover only a few dozen pixels.

Naive whole-image downscaling discards these critical fine-grained features. The standard remedy in literature is **question-conditioned zooming / tile selection** (e.g., scoring tiles via saliency and CLIP, then inspecting top-$k$ crops at native resolution).

In our comprehensive empirical benchmark on **3,080 items of XLRS-Bench** using **Qwen2.5-VL-7B** (detailed in [`materials/main.pdf`](file:///d:/projects/research/vlm/materials/main.pdf)), we evaluated four core methods under matched compute:
1. **Direct**: Whole image in 1 call (downsampled to 1,024 px).
2. **Tiling**: 8 independent grid tiles with text-only voting.
3. **Selection**: Saliency + CLIP question-scored top-5 tiles processed locally.
4. **Proposed**: Selection + explicit cross-tile geometric relation graph (lifting local boxes to global coordinates, deduping seams, emitting direction/distance/containment/intersection edges).

### Empirical Results Summary (from Paper Table 1 & Table 2)

| Method | VLM Calls | Encoded MPix | Prompt Tokens | Wall-time (s/item) | Overall Acc (%) | Relational Acc (%) | Non-Relational Acc (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Direct** | 1.00 | 0.98 | 1,403 | 3.0s | 41.3% | **37.9%** | 42.6% |
| **Tiling** | 9.15 | 7.83 | 11,810 | 5.0s | 37.8% | 34.0% | 39.0% |
| **Selection** | 6.10 | 7.53 | 12,006 | 16.8s | **43.1%** | 33.4% | **46.7%** |
| **Proposed** | 6.10 | 7.53 | 12,455 | 16.9s | 42.7% | 33.4% | 46.2% |
| *Oracle (Direct vs Select)* | *1.0 - 6.1* | - | - | - | **51.2%** | **44.9%** | **53.6%** |

### The Three Core Empirical Discoveries

1. **The Crossover Effect ($p < 10^{-4}$)**:
   - Zooming (Tile Selection) significantly **improves perception/non-relational tasks** (+4.1 pp, from 42.6% to 46.7%, e.g., object color +6.0 pp).
   - Zooming severely **damages spatial/relational reasoning** (-4.5 pp, from 37.9% down to 33.4%).
   - On **Object Spatial Relationship** (500 items), Selection drops performance to **27.2%**, hovering barely above the 25.0% random-choice baseline.
2. **The Null Result of Explicit Geometric Relations (+0.0 pp)**:
   - Supplying an explicit geometric scene graph in text yielded exactly **+0.0 pp on relational tasks** (95% CI $[-2.1, +2.1]$).
   - On perception tasks, adding relation text acted as a **distractor** (-0.5 pp).
3. **The Grounding Bottleneck as the Root Cause**:
   - The frozen 7B VLM prompted as a zero-shot bounding-box extractor returned **no objects for 66% of scenes**.
   - On small-object categories (object color, classification, motion state), the failure rate was **98% to 100%**.
   - Only 21% of scenes produced any cross-tile relations.
4. **The Latency and Cost Overhead**:
   - Selection costs **5.6× the wall time** of Direct (16.8s vs 3.0s).
   - **Local extraction consumes 77% of total runtime** (13.0s out of 16.8s).

---

## 2. Research Mission & New Engineering Objectives

Our goal is to **solve the crossover effect and achieve Pareto-optimal efficiency and accuracy** on ultra-high-resolution remote-sensing multimodal reasoning:

### Objective A: Intelligent Multimodal Routing (Direct vs. Zoom)
- **Insight**: Direct and Selection fail on distinct, complementary subsets of problems. An oracle router achieves **51.2% overall** (a massive +8.1 pp leap over the best single method).
- **Goal**: Develop a lightweight question-conditioned and coarse-visual router that predicts whether a scene requires local zoom or global context.
- **Efficiency Impact**: For questions that don't need zoom, skip the 5 extraction calls, slashing average latency from 16.8s toward ~3.5s while rescuing relational accuracy from the -4.5 pp degradation.

### Objective B: Reliable Grounding via Dedicated Detectors
- **Insight**: The VLM extraction failure (66% null objects) crippled the symbolic relation pipeline.
- **Goal**: Evaluate dedicated open-vocabulary object detectors (YOLO-World, Grounding DINO, oriented remote-sensing bounding-box models) as the grounding engine.

### Objective C: Cross-Scale Topological & Feature Preservation
- **Insight**: Serializing spatial relationships into text predicates failed because text-based graph prompts clutter context without conveying geometric continuity.
- **Goal**: Investigate vision-centric multi-scale fusion: 2D RoPE position encodings, multi-scale visual tokens, coarse-to-fine pyramidal token pruning, and coordinate-conditioned visual prompts.

---

## 3. Formal Research Questions (RQs)

- **RQ 1 (Routing)**: Can a lightweight classifier or LLM prompt router accurately predict whether an ultra-high-resolution question benefits from global overview vs. local zoom, capturing the +8.1 pp oracle gain while cutting average compute by >60%?
- **RQ 2 (Grounding)**: Does replacing zero-shot VLM bounding-box extraction with specialized open-vocabulary remote sensing detectors solve the 66% null-object bottleneck and unlock relational improvements?
- **RQ 3 (Representation)**: How can multi-scale visual features and spatial coordinates be represented within the multimodal sequence to avoid the crossover effect without flooding the token budget?
- **RQ 4 (Efficiency Pareto)**: What is the optimal Pareto curve between encoded megapixels, VLM API/forward calls, and task accuracy across both relational and perceptual remote sensing VQA?

---

## 4. Key Hypotheses & Verification Matrix

| ID | Hypothesis | Proposed Mechanism | Target Metric / Threshold |
| :--- | :--- | :--- | :--- |
| **H1** | Question-conditioned router captures $\ge 70\%$ of the oracle gap ($+5.5\text{ pp}$) | Lightweight text/BERT/DeBERTa classifier on question + options | $\ge 48.5\%$ Overall Acc, $<6.0\text{s}$ mean latency |
| **H2** | Specialized open-vocab detector drops null-object rate from $66\%$ to $<15\%$ | YOLO-World / Grounding DINO fine-tuned on RS / DOTA | Null rate $<15\%$, valid cross-tile graphs $>70\%$ |
| **H3** | Multi-scale visual token injection prevents relational degradation | Global overview tokens + cropped patch tokens with 2D relative position offsets | Relational tasks $\ge 40.0\%$ (vs $33.4\%$ current Selection) |
| **H4** | Coarse-to-fine token pruning maintains perception gains with $3\times$ fewer visual tokens | Text-guided token pruner (LRS-VQA style) | Non-relational acc $\ge 46.0\%$ with $\le 4,000$ tokens |
