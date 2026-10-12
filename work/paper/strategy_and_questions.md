# 🎯 Research Strategy, Journal Roadmap & Open Technical Questions

This document records the publication plan, the two manuscript versions, and the open technical questions for the research project targeting **CVC 2027** and journal publication (5-day sprint).

---

## 1. Dual Publication Strategy (Two Distinct Manuscript Versions)

As decided, we are preparing **two complementary manuscript tracks** targeting journal publication:

### Version 1: The Diagnostic & Empirical Paper (Option A Focus)
- **Working Title**: *"Tile Selection Helps Perception but Hurts Spatial Reasoning in Ultra-High-Resolution Remote Sensing Visual Question Answering"*
- **Core Framing**: A rigorous empirical benchmark study challenging the prevailing assumption in high-resolution computer vision that "zoom is a free lunch".
- **Key Contributions**:
  1. Discovery and formal statistical proof of the **crossover effect** ($p < 10^{-4}$): zoom increases perception by $+4.1\text{ pp}$ but drops spatial relations by $-4.5\text{ pp}$ on XLRS-Bench.
  2. The **explicit relation null result**: showing that serializing geometric relations into natural language text yields $+0.0\text{ pp}$ and acts as a semantic distractor.
  3. Diagnosing the **grounding bottleneck**: proving that zero-shot VLM object extraction returns no objects for $66\%$ of scenes.
  4. Establishing the **$51.2\%$ oracle upper bound** demonstrating that routing between global overview and local crops unlocks major performance gains.

### Version 2: The Methodological Solution Paper (Option B Focus)
- **Working Title**: *"Beyond Zoom: Hierarchical Dual-Stream Anchoring and Dynamic Routing for Ultra-High-Resolution Remote Sensing Multimodal Reasoning"*
- **Core Framing**: A novel, end-to-end architectural system that actively resolves the crossover dilemma and eliminates the grounding bottleneck.
- **Key Contributions**:
  1. **Dual-Stream Global-Local Anchoring**: Prepending low-resolution overview tokens to local crops, permanently preventing "Visual Myopia".
  2. **Fast Decoupled Grounding Engine**: Replacing the 66% null-object failure with open-vocabulary detection (YOLO-World / Grounding DINO) running in $<20\text{ms}$.
  3. **Visual Set-of-Mark (SoM) Relational Prompting**: Bypassing text-serialized relation distractors by painting symbolic markers directly on candidate targets.
  4. **Logit Margin Uncertainty Gating**: Calibrated routing that dispatches easy/relational queries to the overview ($3.0\text{s}$) and complex perception queries to zoom ($4.2\text{s}$), cutting compute by $>70\%$ and beating the $51.2\%$ oracle benchmark.

---

## 2. Open Technical Questions Tracker (Saved for Deep-Dive)

### Question 2: The Grounding Engine Strategy
- **Issue**: Zero-shot VLM prompting on `Qwen2.5-VL-7B` fails to locate objects in $66\%$ of scenes ($98\%-100\%$ on small objects like cars and storage tanks).
- **Options to finalize**:
  - *Option 2A (Hybrid Modular)*: Integrate YOLO-World-v2 / Grounding DINO ($19\text{ms}$ latency, $<8\%$ null rate, open-vocabulary text conditioning).
  - *Option 2B (Fine-Tuned VLM / Prompt Engineering)*: Keep pure VLM autoregressive heads but fine-tune/prompt on oriented bounding boxes or multi-scale patch queries.
- **Status**: **Pending Discussion**.

### Question 3: Spatial Relation Representation
- **Issue**: Serializing geometric relation triples into natural language text produced $+0.0\text{ pp}$ on relations and $-4.1\text{ pp}$ on perception (semantic distractor effect).
- **Options to finalize**:
  - *Option 3A (Visual Overlays)*: Set-of-Mark (SoM) visual alphanumeric masks painted on image pixels.
  - *Option 3B (Architectural Token Concatenation)*: Dual-stream token concatenation with 2D-RoPE spatial coordinate offsets.
  - *Option 3C (Neurosymbolic Execution)*: Deterministic Python execution engine (ViperGPT style) for exact Euclidean distance/cardinal direction math.
- **Status**: **Pending Discussion**.

---

## 3. Timeline & Target Venue
- **Target Venue**: Computer Vision Conference 2027 (CVC 2027) + Journal Extension.
- **Execution Sprint**: 5 days maximum to finalize manuscripts, benchmarking, and figures.
