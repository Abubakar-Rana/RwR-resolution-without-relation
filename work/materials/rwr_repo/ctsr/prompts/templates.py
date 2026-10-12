"""Prompt templates.

The experimental logic of the study is encoded in these templates, so they are
kept in one file and written to make the controlled comparison auditable.

The critical invariant (plan sections 6 and 8): the Baseline-3 prompt and the
Proposed prompt are produced by the SAME function, `aggregation_prompt`, and
differ ONLY by the presence of the SPATIAL RELATIONS block. Identical
instructions, identical answer-format text, identical object evidence, identical
image inputs. If you edit one arm's wording you must edit the other, otherwise
the ablation measures prompt phrasing rather than spatial structure.

Answer-format instructions are written to be machine-parseable first
(`ctsr.eval.parsing` consumes them) and are kept byte-identical across arms so
that parse-failure rates are comparable.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence

# --------------------------------------------------------------------------
# Answer-format contracts. Shared verbatim by every arm.
# --------------------------------------------------------------------------

MCQ_FORMAT = (
    "Respond with ONLY the single letter of the correct option, on its own line, "
    "in the form: ANSWER: X"
)

COUNT_FORMAT = (
    "Respond with ONLY the final integer count, on its own line, "
    "in the form: ANSWER: <integer>"
)

GROUNDING_FORMAT = (
    "Respond with ONLY the bounding box of the requested target, on its own line, "
    "in the form: ANSWER: [x1, y1, x2, y2]\n"
    "Use integer coordinates on a 0-1000 grid measured over the ENTIRE image, "
    "where (0,0) is the top-left corner and (1000,1000) is the bottom-right corner."
)

CAPTION_FORMAT = (
    "Write a single detailed paragraph describing the scene: the land-use types "
    "present, the salient objects and their approximate locations, and the spatial "
    "arrangement between them. Do not use bullet points and do not mention tiles, "
    "crops or coordinates."
)


def format_instruction(family: str) -> str:
    """The answer-format contract for a task family."""
    fam = str(family or "mcq").lower()
    if fam.startswith("caption"):
        return CAPTION_FORMAT
    if fam.startswith("grounding"):
        return GROUNDING_FORMAT
    if fam == "counting":
        return COUNT_FORMAT
    return MCQ_FORMAT


def _question_block(question: str, options: Optional[Sequence[str]],
                    family: str) -> str:
    """Question + options, rendered identically for every arm."""
    parts: List[str] = []
    q = str(question or "").strip()
    if not q and str(family).startswith("caption"):
        q = "Describe this remote sensing image in detail."
    parts.append("QUESTION: {}".format(q))
    if options:
        letters = [chr(ord("A") + i) for i in range(len(options))]
        parts.append("OPTIONS:")
        parts.extend("{}. {}".format(l, o) for l, o in zip(letters, options))
    return "\n".join(parts)


def _answer_family(family: str, options: Optional[Sequence[str]]) -> str:
    """A question with options is answered as MCQ regardless of its task family."""
    if options:
        return "mcq"
    return str(family or "mcq").lower()


# --------------------------------------------------------------------------
# Baseline 1: direct inference on the whole image
# --------------------------------------------------------------------------

def direct_prompt(question: str, options: Optional[Sequence[str]] = None,
                  family: str = "mcq", n_images: int = 1) -> str:
    fam = _answer_family(family, options)
    imgs = ("You are shown one ultra-high-resolution remote sensing image."
            if n_images <= 1 else
            "You are shown {} ultra-high-resolution remote sensing images of the "
            "same area, in chronological order.".format(n_images))
    return "\n\n".join([
        imgs,
        _question_block(question, options, fam),
        format_instruction(fam),
    ])


# --------------------------------------------------------------------------
# Baseline 2: independent tiles, then answer-level aggregation
# --------------------------------------------------------------------------

def tile_answer_prompt(question: str, options: Optional[Sequence[str]],
                       family: str, tile_index: int, n_tiles: int,
                       tile_box: Optional[Sequence[int]] = None) -> str:
    """Ask the question of one tile in isolation.

    Baseline 2 deliberately withholds the tile's position in the scene, which is
    what makes it the "independent tiles" control: any cross-tile structure it
    recovers would have to come from the aggregation step, not from geometry.
    """
    fam = _answer_family(family, options)
    where = ""
    if tile_box is not None:
        where = " covering image region ({}, {}) to ({}, {})".format(*tile_box)
    return "\n\n".join([
        "You are shown crop {} of {} from a larger remote sensing image{}. "
        "Answer using only what is visible in this crop. If the crop does not "
        "contain enough information, say UNKNOWN.".format(
            tile_index + 1, n_tiles, where),
        _question_block(question, options, fam),
        format_instruction(fam) + "\nIf the crop is insufficient, respond: ANSWER: UNKNOWN",
    ])


def tile_vote_prompt(question: str, options: Optional[Sequence[str]],
                     family: str, tile_answers: Sequence[str]) -> str:
    """Text-only reconciliation of per-tile answers (Baseline 2's aggregator)."""
    fam = _answer_family(family, options)
    listing = "\n".join(
        "- crop {}: {}".format(i + 1, str(a).strip().replace("\n", " ")[:300])
        for i, a in enumerate(tile_answers)
    ) or "- (no usable crop answers)"
    return "\n\n".join([
        "A large remote sensing image was split into independent crops and each "
        "crop was analysed separately. Below are the per-crop answers. Reconcile "
        "them into one final answer for the whole image. For counting questions, "
        "be aware that crops overlap, so the same object may appear in more than "
        "one crop.",
        "PER-CROP ANSWERS:\n" + listing,
        _question_block(question, options, fam),
        format_instruction(fam),
    ])


# --------------------------------------------------------------------------
# Local extraction (shared by Baseline 3 and Proposed)
# --------------------------------------------------------------------------

def local_extraction_prompt(question: str, tile_box: Sequence[int],
                            image_size: Sequence[int],
                            max_objects: int = 12,
                            keywords: Optional[Sequence[str]] = None) -> str:
    """Extract objects + tile-local boxes from one high-resolution crop.

    Boxes are requested on a 0-1000 grid over THE CROP, and lifted to global
    coordinates by `ctsr.spatial.coords`. We ask for crop-relative coordinates
    rather than global ones on purpose: asking a VLM to do the coordinate
    arithmetic itself is a known failure mode, and doing it in code is exact.

    The prompt names the question so extraction is question-conditioned, but it
    also asks for prominent objects regardless, so that the object list is not so
    narrow that a relational question has nothing to relate.
    """
    focus = ""
    if keywords:
        focus = ("\nPay particular attention to anything resembling: {}."
                 .format(", ".join(str(k) for k in keywords[:10])))
    return "\n\n".join([
        "You are shown a high-resolution crop taken from a much larger remote "
        "sensing image of {} x {} pixels. This crop covers the region ({}, {}) to "
        "({}, {}) of the full image.".format(
            image_size[0], image_size[1], tile_box[0], tile_box[1],
            tile_box[2], tile_box[3]),
        "TASK CONTEXT (the question that will later be answered about the whole "
        "image): {}".format(str(question or "Describe the scene.").strip()) + focus,
        "List the distinct, clearly visible objects and regions in this crop that "
        "are relevant to the task context, plus any other prominent objects. "
        "Report at most {} items.\n"
        "For each item give a label, a bounding box, and any confidently visible "
        "attributes (colour, condition, motion state).\n"
        "Bounding boxes must be integers on a 0-1000 grid measured over THIS CROP "
        "ONLY: (0,0) is the crop's top-left corner and (1000,1000) its "
        "bottom-right corner.\n"
        "Do not report anything you cannot actually see. Do not guess.".format(max_objects),
        'Respond with ONLY a JSON object, no commentary, in exactly this form:\n'
        '{"objects": [{"label": "building", "bbox": [120, 340, 260, 470], '
        '"attributes": {"color": "grey"}}]}\n'
        'If the crop contains nothing relevant, respond: {"objects": []}',
    ])


def tile_relevance_prompt(question: str, n_tiles: int) -> str:
    """Optional VLM-based tile scoring (see tiling.selection.VLMScorer)."""
    return "\n\n".join([
        "You are shown {} thumbnails, each a different region of one large remote "
        "sensing image, in order.".format(n_tiles),
        "QUESTION TO BE ANSWERED ABOUT THE FULL IMAGE: {}".format(
            str(question or "Describe the scene.").strip()),
        "For each thumbnail, rate from 0 to 10 how likely it is to contain "
        "evidence needed to answer the question.",
        "Respond with ONLY {} integers separated by commas, in thumbnail order, "
        "and nothing else.".format(n_tiles),
    ])


# --------------------------------------------------------------------------
# Final aggregation: THE controlled comparison
# --------------------------------------------------------------------------

def aggregation_prompt(
    question: str,
    options: Optional[Sequence[str]],
    family: str,
    object_block: str,
    relation_block: Optional[str] = None,
    n_images_shown: int = 0,
    overview_shown: bool = True,
    n_regions: int = 0,
) -> str:
    """Final-stage prompt for Baseline 3 (relation_block=None) and Proposed.

    Passing `relation_block=None` yields the ablated arm. Everything else about
    the prompt is generated by the same code path, which is what makes the
    difference attributable to the relation representation.
    """
    fam = _answer_family(family, options)

    if overview_shown and n_images_shown:
        vision = ("You are shown a downscaled overview of the whole scene followed "
                  "by {} high-resolution crops of the regions selected as most "
                  "relevant.".format(n_images_shown - 1 if n_images_shown > 1 else n_images_shown))
    elif n_images_shown:
        vision = ("You are shown {} high-resolution crops of the regions selected "
                  "as most relevant.".format(n_images_shown))
    else:
        vision = "You are given a structured description of the scene."

    header = (
        "{}\nThe following structured evidence was extracted from {} "
        "high-resolution region(s) of the full image and registered into a single "
        "global coordinate system for the whole scene.".format(vision, n_regions)
    )

    evidence: List[str] = [object_block.strip()]
    if relation_block:
        evidence.append(relation_block.strip())

    if relation_block:
        guidance = (
            "Use the overview for scene context, the crops for fine detail, and the "
            "listed objects and spatial relations for anything that depends on where "
            "things are relative to each other. The relations are computed "
            "geometrically from the registered coordinates and are reliable; "
            "relations marked 'cross-tile' hold between objects that were observed "
            "in different crops."
        )
    else:
        guidance = (
            "Use the overview for scene context, the crops for fine detail, and the "
            "listed objects for anything that depends on where things are. Object "
            "coordinates are given in the global frame of the whole image, so you "
            "may compare them."
        )

    caveat = (
        "The evidence list may be incomplete. If it does not settle the question, "
        "rely on what you can see in the images. Do not invent objects."
    )

    return "\n\n".join([
        header,
        "\n\n".join(evidence),
        guidance,
        caveat,
        _question_block(question, options, fam),
        format_instruction(fam),
    ])


def object_block_text(lines: Sequence[str], header: str) -> str:
    """Wrap object lines with a header, matching SceneGraph.to_text's layout."""
    body = "\n".join(lines) if lines else "(none detected)"
    return "{}\n{}".format(header, body)


# --------------------------------------------------------------------------
# Flood case study (plan section 11)
# --------------------------------------------------------------------------

FLOOD_QUESTION_TEMPLATES: List[str] = [
    "Which {facility} are located inside the flooded area?",
    "How many {facility} are within the inundated region?",
    "Is any {facility} adjacent to the flood boundary but not yet inundated?",
    "Which access road to the nearest {facility} is cut off by the flood water?",
]


def flood_case_prompt(question: str, object_block: str,
                      relation_block: Optional[str] = None,
                      n_regions: int = 0) -> str:
    """Open-ended, evidence-grounded answer for the qualitative demonstration.

    Deliberately asks for object ids so that the answer can be checked against
    the graph rather than taken on trust - the point of the demonstration is that
    the answer is traceable to specific detections.
    """
    evidence = [object_block.strip()]
    if relation_block:
        evidence.append(relation_block.strip())
    return "\n\n".join([
        "You are a flood-impact analyst working from an ultra-high-resolution "
        "satellite image. Structured evidence extracted from {} high-resolution "
        "regions, registered into one global coordinate system, follows."
        .format(n_regions),
        "\n\n".join(evidence),
        "QUESTION: {}".format(str(question).strip()),
        "Answer in at most four sentences. Cite the object ids (for example #12) "
        "that support your answer. If the evidence is insufficient, say so "
        "explicitly instead of guessing.",
    ])
