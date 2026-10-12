# Algorithmic Next Steps & Experimental Roadmap

Based on the empirical findings of the **RwR (Resolution without Relation)** baseline study and our comprehensive **60-paper systematic literature review**, this document defines the concrete algorithmic implementation and benchmarking roadmap.

---

## 🗺️ Architectural Evolution Overview

```mermaid
flowchart TD
    subgraph Phase 1: Intelligent Router
        Q[Input Question + 8.5K Scene] --> ROUTE{Multimodal Router<br/>Lightweight Classifier / Prior}
        ROUTE -->|Relational / Macro Query| DIR[Direct Route<br/>Whole-scene Overview<br/>Latency: 3.0s | Acc: 37.9% Rel]
        ROUTE -->|Perceptual / Attribute Query| ZOOM[Zoom Route<br/>High-detail Crops<br/>Latency: <4.0s | Acc: 46.7% Non-Rel]
    end

    subgraph Phase 2: Fast Grounding Engine
        ZOOM --> YW[YOLO-World / Grounding DINO<br/>Replaces 5 VLM calls<br/>Latency: 0.15s vs 13.0s<br/>Null Rate: <10% vs 66%]
    end

    subgraph Phase 3: Visual Set-of-Mark Grounding
        YW --> SOM[Set-of-Mark Annotation<br/>Overlays IDs on Crops<br/>Zero Coordinate Text Hallucination]
        SOM --> VLM[Final Qwen2.5-VL-7B Call<br/>Overview + Marked Crops + Answer]
    end

    DIR --> OUT[Final Multiple-Choice Answer]
    VLM --> OUT
```

---

## 📋 Phase 1: Multi-Modal Router Implementation (Weeks 1–2)

### Objective
Capture the **+8.1 pp Oracle gain** (moving from 43.1% to ~48.5% - 51.2%) while reducing average latency from 16.8s to **<4.0s per item**.

### Concrete Deliverables:
1. **Task Prior Router** (`src/routing/prior_router.py`):
   - Zero-latency heuristic routing relational task categories to Direct and perception categories to Selection.
   - Theoretical baseline accuracy: $\approx 48.3\%$ overall.
2. **Text-Classifier Router** (`src/routing/classifier_router.py`):
   - Train a ModernBERT / DeBERTa-v3-small model on XLRS-Bench question embeddings to predict whether Direct or Selection wins.
   - Inference latency: $<5\text{ ms}$.
3. **Cascaded Confidence Router** (`src/routing/cascaded_router.py`):
   - Runs Direct first ($3.0\text{s}$). If top-1 vs top-2 logit margin exceeds threshold $\tau$, return answer. Otherwise escalate to Zoom.

---

## 📋 Phase 2: Fast Grounding Engine with YOLO-World (Weeks 2–3)

### Objective
Eliminate the **66% null-object extraction failure** and slash local extraction runtime from **13.0s down to <0.15s**.

### Concrete Deliverables:
1. **YOLO-World Grounding Interface** (`src/grounding/yolo_world_grounder.py`):
   - Extract candidate object nouns from question text via fast rule/spacy/LLM prompt.
   - Feed vocabulary to YOLO-World for sub-30ms detection per tile.
2. **Bounding Box Seam Deduplication** (`src/grounding/rotated_dedup.py`):
   - Upgrade `ctsr/spatial/dedup.py` to handle seam overlaps and filter edge-boundary duplicates.
3. **Evaluation on 800 Relational Items**:
   - Re-evaluate the relation graph pipeline with valid, non-null object detections to determine the true upper bound of cross-tile geometric graphs.

---

## 📋 Phase 3: Visual Set-of-Mark Prompting & Token Compression (Weeks 3–4)

### Objective
Eliminate text-coordinate distraction errors (-4.1 pp on perception) and compress crop token budgets by 75%.

### Concrete Deliverables:
1. **Visual Mark Annotator** (`src/grounding/set_of_mark.py`):
   - Draw visible bounding boxes with clean alphanumeric tags (`[1]`, `[2]`, `[3]`) directly onto high-resolution crops and low-resolution thumbnails.
   - Prompt Qwen2.5-VL to refer to entities by tag ID rather than guessing numerical coordinates.
2. **Pixel Shuffle 2x2 Connector** (`src/models/projectors/pixel_shuffle.py`):
   - Implement InternVL-style 2x2 spatial unshuffle, compressing 1,024 crop tokens down to 256 tokens per crop while retaining 2D spatial arrangement.

---

## 📋 Phase 4: Controlled Benchmark & Manuscript Preparation (Weeks 4–5)

### Objective
Execute full compute-matched paired statistical benchmarking on XLRS-Bench Lite (2,983 scored items) and draft updated research paper.

### Evaluation Protocol:
- **Baseline vs Proposed Contrast**:
  - Baseline 1: Direct (whole image)
  - Baseline 2: Tiling (grid)
  - Baseline 3: Selection (saliency + CLIP)
  - Baseline 4: Proposed RwR (Selection + text relations)
  - **Proposed 5: Routed Architecture (Router + YOLO-World + Set-of-Mark)**
- **Statistical Tests**:
  - Paired McNemar exact test ($p$-value).
  - 10,000-sample bootstrap confidence intervals ($95\%$ CIs).
  - Compute-matched cost accounting: wall time (s/item), VLM calls, encoded MPix, prompt tokens.
