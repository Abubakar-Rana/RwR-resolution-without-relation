# The Grounding Failure Audit: Why Symbolic Relations Had a Null Effect

In the RwR paper, the primary confirmatory hypothesis stated that explicit geometric relations would improve relational reasoning. The experiment proved this false ($+0.0\text{ pp}$). This audit details the empirical causes of this failure.

---

## 1. The 66% Null Extraction Rate

The pipeline relied on prompting a frozen general-purpose VLM (`Qwen2.5-VL-7B-Instruct`) to detect objects within each selected tile and output JSON bounding boxes:
$$\text{Crop} \xrightarrow{\text{Frozen VLM}} \{\text{"label": str, "box": } [y_1, x_1, y_2, x_2]\}^{N}$$

### Empirical Failure Rates Across Tasks
- **Across All 3,080 Scenes**: **66% of scenes** returned **zero objects** across all five selected crops.
- **Small-Object Perception Tasks**:
  - *Object Colour*: **100% of scenes produced 0 objects**
  - *Object Motion State*: **100% of scenes produced 0 objects**
  - *Object Classification*: **98% of scenes produced 0 objects**
- **Relational Tasks**:
  - *Regional Counting*: 49% had 0 objects
  - *Complex Counting*: 48% had 0 objects
  - *Spatial Relationship*: 37% had 0 objects
  - *Route Planning*: 28% had 0 objects

Only **21% of scenes** yielded any cross-tile relationships!

---

## 2. Parsing vs. Perceptual Failure

Was this failure caused by bad JSON parsing or syntax errors?
**No.**
- Only **1.6%** of the 19,481 output items lacked a parseable bounding box format.
- The failure was genuinely perceptual: the model simply stated that no objects matching the prompt were visible or emitted empty arrays `[]`.
- This proves that prompting a general-domain 7B VLM zero-shot to act as a precision object detector on ultra-high-resolution aerial imagery is fundamentally flawed.

---

## 3. Label Hallucination & Question Mimicry

When the VLM did output object labels:
- It frequently copied the question verbatim into the label text (e.g., labeling a building as `"the building with the red pyramid roof to the parking lot on the left"`).
- This created self-referential, noisy node labels in the scene graph.

---

## 4. The Distractor Effect on Perception Tasks

When relations were present:
- On relational items with cross-tile edges ($n = 247$), relations produced an indicative $+2.8\text{ pp}$ change ($95\%$ CI $[-2.0, +7.7]$).
- But on non-relational perception items ($n = 293$), relations caused a statistically significant drop of **$-4.1\text{ pp}$** ($p = 0.02$).
- In text prompts, dozens of lines describing spatial relations (e.g. `obj_1 is north of obj_2 by 450 px`) flooded the attention context, confusing the model when it only needed to inspect the color or category of a single object.

---

## 5. Architectural Implications for Our New Research

1. **Abandon Zero-Shot VLM Detector Calls**:
   Zero-shot VLM prompting cannot ground small aerial objects.
2. **Adopt Dedicated Open-Vocabulary Detectors**:
   Deploy specialized remote-sensing / open-vocabulary detectors (e.g., YOLO-World, Grounding DINO, DOTA-trained oriented models) designed specifically for dense aerial features.
3. **Condition Relation Injection on Question Type**:
   Never inject spatial relational text into non-relational perception queries.
