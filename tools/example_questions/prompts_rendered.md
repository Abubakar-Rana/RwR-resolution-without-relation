# Prompts sent to Qwen2.5-VL-7B

Rendered with the run's own templates (`ctsr/prompts/templates.py`) for one real Object Spatial Relationship item. The object and relation lines are a short excerpt for illustration; the real blocks list every detected object and up to 220 relations.

## B1 direct (1 call)

```text
You are shown one ultra-high-resolution remote sensing image.

QUESTION: In the image, the two smaller green rectangular greenhouses located towards the upper right are positioned in which direction relative to the larger multi-unit residential area?
OPTIONS:
A. On the left side
B. Top left corner
C. To the right
D. Above

Respond with ONLY the single letter of the correct option, on its own line, in the form: ANSWER: X
```

## B2 per-tile answer (x8)

```text
You are shown crop 1 of 8 from a larger remote sensing image. Answer using only what is visible in this crop. If the crop does not contain enough information, say UNKNOWN.

QUESTION: In the image, the two smaller green rectangular greenhouses located towards the upper right are positioned in which direction relative to the larger multi-unit residential area?
OPTIONS:
A. On the left side
B. Top left corner
C. To the right
D. Above

Respond with ONLY the single letter of the correct option, on its own line, in the form: ANSWER: X
If the crop is insufficient, respond: ANSWER: UNKNOWN
```

## Local extraction, B3 and Proposed (x5)

```text
You are shown a high-resolution crop taken from a much larger remote sensing image of 4097 x 4096 pixels. This crop covers the region (0, 2048) to (1024, 3072) of the full image.

TASK CONTEXT (the question that will later be answered about the whole image): In the image, the two smaller green rectangular greenhouses located towards the upper right are positioned in which direction relative to the larger multi-unit residential area?
Pay particular attention to anything resembling: building, circular.

List the distinct, clearly visible objects and regions in this crop that are relevant to the task context, plus any other prominent objects. Report at most 12 items.
For each item give a label, a bounding box, and any confidently visible attributes (colour, condition, motion state).
Bounding boxes must be integers on a 0-1000 grid measured over THIS CROP ONLY: (0,0) is the crop's top-left corner and (1000,1000) its bottom-right corner.
Do not report anything you cannot actually see. Do not guess.

Respond with ONLY a JSON object, no commentary, in exactly this form:
{"objects": [{"label": "building", "bbox": [120, 340, 260, 470], "attributes": {"color": "grey"}}]}
If the crop contains nothing relevant, respond: {"objects": []}
```

## Final call, B3 (no relation block)

```text
You are shown a downscaled overview of the whole scene followed by 3 high-resolution crops of the regions selected as most relevant.
The following structured evidence was extracted from 5 high-resolution region(s) of the full image and registered into a single global coordinate system for the whole scene.

DETECTED OBJECTS (global coordinates, 0-1000 grid over the whole image):
#0 building box=(462,779,625,952)
#4 white circular building box=(298,560,343,586)

Use the overview for scene context, the crops for fine detail, and the listed objects for anything that depends on where things are. Object coordinates are given in the global frame of the whole image, so you may compare them.

The evidence list may be incomplete. If it does not settle the question, rely on what you can see in the images. Do not invent objects.

QUESTION: In the image, the two smaller green rectangular greenhouses located towards the upper right are positioned in which direction relative to the larger multi-unit residential area?
OPTIONS:
A. On the left side
B. Top left corner
C. To the right
D. Above

Respond with ONLY the single letter of the correct option, on its own line, in the form: ANSWER: X
```

## Final call, Proposed (with relation block)

```text
You are shown a downscaled overview of the whole scene followed by 3 high-resolution crops of the regions selected as most relevant.
The following structured evidence was extracted from 5 high-resolution region(s) of the full image and registered into a single global coordinate system for the whole scene.

DETECTED OBJECTS (global coordinates, 0-1000 grid over the whole image):
#0 building box=(462,779,625,952)
#4 white circular building box=(298,560,343,586)

SPATIAL RELATIONS (computed geometrically from the global coordinates):
#0 building contains #8 white circular building [overlap 100%]
#7 white circular building is to the south-west of #4 white circular building [779 px; cross-tile]

Use the overview for scene context, the crops for fine detail, and the listed objects and spatial relations for anything that depends on where things are relative to each other. The relations are computed geometrically from the registered coordinates and are reliable; relations marked 'cross-tile' hold between objects that were observed in different crops.

The evidence list may be incomplete. If it does not settle the question, rely on what you can see in the images. Do not invent objects.

QUESTION: In the image, the two smaller green rectangular greenhouses located towards the upper right are positioned in which direction relative to the larger multi-unit residential area?
OPTIONS:
A. On the left side
B. Top left corner
C. To the right
D. Above

Respond with ONLY the single letter of the correct option, on its own line, in the form: ANSWER: X
```
