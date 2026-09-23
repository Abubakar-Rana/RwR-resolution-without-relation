"""Metrics.

Matched to what XLRS-Bench reports (verified from the paper):
  * VQA / MCQ        accuracy
  * visual grounding precision at IoU 0.5 and IoU 0.7
  * detailed captioning  BLEU-1..4, ROUGE_L, METEOR

BLEU and ROUGE-L are implemented here in pure Python so a run never silently
loses its caption numbers to a missing package. METEOR needs NLTK+WordNet; when
unavailable it is reported as None, never as 0.0 and never approximated by
something else, because a fabricated metric value is worse than a missing one.

Counting also reports MAE and off-by-one accuracy alongside exact accuracy. Those
are only computed for open-ended counting; when a counting task is delivered as
MCQ (as in the lite split) accuracy is the only meaningful figure and the numeric
fields stay None.
"""
from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Tuple

from ..utils.logging_utils import get_logger
from .parsing import (MCQParse, gt_captions, gt_count, gt_letter, parse_bbox,
                      parse_count, parse_gt_bbox, parse_mcq)

LOG = get_logger("ctsr.eval.metrics")

_NLTK_METEOR_STATE: Dict[str, Any] = {"checked": False, "available": False}


# --------------------------------------------------------------------------
# Tokenisation shared by the caption metrics
# --------------------------------------------------------------------------

def tokenize(text: str) -> List[str]:
    return re.findall(r"[a-z0-9]+", str(text or "").lower())


# --------------------------------------------------------------------------
# BLEU
# --------------------------------------------------------------------------

def _ngrams(tokens: Sequence[str], n: int) -> Counter:
    return Counter(tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1))


def bleu(candidate: str, references: Sequence[str], max_n: int = 4,
         smooth: bool = True) -> Dict[str, Optional[float]]:
    """Corpus-style BLEU-1..max_n for a single sentence against >=1 references.

    Uses add-one smoothing on higher-order precisions (Chen & Cherry method 2),
    without which a single short caption missing one 4-gram scores exactly 0 and
    the sentence-level mean becomes uninformative.
    """
    cand = tokenize(candidate)
    refs = [tokenize(r) for r in references if str(r).strip()]
    out: Dict[str, Optional[float]] = {"bleu_{}".format(n): None for n in range(1, max_n + 1)}
    if not cand or not refs:
        return out

    # Brevity penalty against the closest reference length.
    ref_len = min((len(r) for r in refs), key=lambda l: (abs(l - len(cand)), l))
    bp = 1.0 if len(cand) > ref_len else math.exp(1 - ref_len / max(1, len(cand)))

    log_precisions: List[float] = []
    for n in range(1, max_n + 1):
        cand_ng = _ngrams(cand, n)
        total = sum(cand_ng.values())
        if total == 0:
            out["bleu_{}".format(n)] = 0.0
            log_precisions.append(float("-inf"))
            continue
        max_ref = Counter()
        for r in refs:
            for ng, c in _ngrams(r, n).items():
                if c > max_ref[ng]:
                    max_ref[ng] = c
        clipped = sum(min(c, max_ref[ng]) for ng, c in cand_ng.items())
        if smooth and n > 1:
            p = (clipped + 1.0) / (total + 1.0)
        else:
            p = clipped / total
        log_precisions.append(math.log(p) if p > 0 else float("-inf"))
        geo = [lp for lp in log_precisions[:n]]
        if any(lp == float("-inf") for lp in geo):
            out["bleu_{}".format(n)] = 0.0
        else:
            out["bleu_{}".format(n)] = bp * math.exp(sum(geo) / n)
    return out


# --------------------------------------------------------------------------
# ROUGE-L
# --------------------------------------------------------------------------

def _lcs_length(a: Sequence[str], b: Sequence[str]) -> int:
    """LCS length with an O(min(n,m)) rolling row."""
    if not a or not b:
        return 0
    if len(a) < len(b):
        a, b = b, a
    prev = [0] * (len(b) + 1)
    for x in a:
        cur = [0] * (len(b) + 1)
        for j, y in enumerate(b, 1):
            cur[j] = prev[j - 1] + 1 if x == y else max(prev[j], cur[j - 1])
        prev = cur
    return prev[len(b)]


def rouge_l(candidate: str, references: Sequence[str], beta: float = 1.2) -> Optional[float]:
    """ROUGE-L F-measure, taking the best reference."""
    cand = tokenize(candidate)
    refs = [tokenize(r) for r in references if str(r).strip()]
    if not cand or not refs:
        return None
    best = 0.0
    for ref in refs:
        l = _lcs_length(cand, ref)
        if l == 0:
            continue
        p = l / len(cand)
        r = l / len(ref)
        denom = r + (beta ** 2) * p
        if denom > 0:
            best = max(best, ((1 + beta ** 2) * p * r) / denom)
    return best


# --------------------------------------------------------------------------
# METEOR (optional dependency)
# --------------------------------------------------------------------------

def _meteor_available() -> bool:
    if _NLTK_METEOR_STATE["checked"]:
        return bool(_NLTK_METEOR_STATE["available"])
    _NLTK_METEOR_STATE["checked"] = True
    try:
        import nltk
        from nltk.translate.meteor_score import meteor_score  # noqa: F401
        # WordNet must actually be downloaded, not merely importable.
        from nltk.corpus import wordnet
        wordnet.synsets("test")
        _NLTK_METEOR_STATE["available"] = True
    except Exception as exc:
        LOG.warning(
            "METEOR unavailable (%s). Caption METEOR will be reported as null, not 0. "
            "To enable it: pip install nltk && python -c "
            "\"import nltk; nltk.download('wordnet'); nltk.download('omw-1.4')\"",
            exc,
        )
        _NLTK_METEOR_STATE["available"] = False
    return bool(_NLTK_METEOR_STATE["available"])


def meteor(candidate: str, references: Sequence[str]) -> Optional[float]:
    """METEOR via NLTK, or None when NLTK/WordNet are unavailable."""
    if not _meteor_available():
        return None
    cand = tokenize(candidate)
    refs = [tokenize(r) for r in references if str(r).strip()]
    if not cand or not refs:
        return None
    try:
        from nltk.translate.meteor_score import meteor_score
        return float(meteor_score(refs, cand))
    except Exception as exc:
        LOG.warning("METEOR computation failed: %s", exc)
        return None


def caption_metrics(candidate: str, references: Sequence[str]) -> Dict[str, Optional[float]]:
    out: Dict[str, Optional[float]] = {}
    out.update(bleu(candidate, references, max_n=4))
    out["rouge_l"] = rouge_l(candidate, references)
    out["meteor"] = meteor(candidate, references)
    return out


# --------------------------------------------------------------------------
# Grounding
# --------------------------------------------------------------------------

def box_iou(a: Sequence[float], b: Sequence[float]) -> float:
    ix1, iy1 = max(a[0], b[0]), max(a[1], b[1])
    ix2, iy2 = min(a[2], b[2]), min(a[3], b[3])
    iw, ih = ix2 - ix1, iy2 - iy1
    if iw <= 0 or ih <= 0:
        return 0.0
    inter = iw * ih
    ua = max(0.0, a[2] - a[0]) * max(0.0, a[3] - a[1])
    ub = max(0.0, b[2] - b[0]) * max(0.0, b[3] - b[1])
    union = ua + ub - inter
    return float(inter / union) if union > 0 else 0.0


def _to_unit(box: Sequence[float], image_size: Optional[Tuple[int, int]]) -> Optional[Tuple[float, float, float, float]]:
    """Put a box in a comparable [0,1] frame.

    Prediction and ground truth may use different conventions (0-1000 grid vs raw
    pixels), so both are normalised before IoU. Returns None when the convention
    cannot be determined, which makes the sample unscorable rather than scored
    against a mismatched frame.
    """
    vals = [float(v) for v in box[:4]]
    mx = max(abs(v) for v in vals) if vals else 0.0
    if mx <= 1.5:
        return (vals[0], vals[1], vals[2], vals[3])
    if image_size and mx > 1000.0 * 1.02:
        w, h = float(image_size[0]), float(image_size[1])
        if w > 0 and h > 0:
            return (vals[0] / w, vals[1] / h, vals[2] / w, vals[3] / h)
        return None
    if mx <= 1000.0 * 1.02:
        return (vals[0] / 1000.0, vals[1] / 1000.0, vals[2] / 1000.0, vals[3] / 1000.0)
    if image_size:
        w, h = float(image_size[0]), float(image_size[1])
        if w > 0 and h > 0:
            return (vals[0] / w, vals[1] / h, vals[2] / w, vals[3] / h)
    return None


def grounding_score(pred_text: str, answer_raw: Any,
                    image_size: Optional[Tuple[int, int]] = None,
                    thresholds: Sequence[float] = (0.5, 0.7)) -> Dict[str, Any]:
    """IoU and per-threshold hits for one grounding item."""
    pred = parse_bbox(pred_text)
    gt = parse_gt_bbox(answer_raw)
    out: Dict[str, Any] = {
        "iou": None, "parse_failed": pred is None, "scorable": gt is not None,
    }
    for t in thresholds:
        out["acc@{}".format(t)] = None
    if gt is None:
        return out
    if pred is None:
        out["iou"] = 0.0
        for t in thresholds:
            out["acc@{}".format(t)] = False
        return out

    pu = _to_unit(pred, image_size)
    gu = _to_unit(gt, image_size)
    if pu is None or gu is None:
        out["iou"] = None
        out["scorable"] = False
        return out

    val = box_iou(pu, gu)
    out["iou"] = val
    for t in thresholds:
        out["acc@{}".format(t)] = bool(val >= t)
    return out


# --------------------------------------------------------------------------
# Per-sample scoring entry point
# --------------------------------------------------------------------------

@dataclass
class ScoreResult:
    correct: Optional[bool] = None
    parsed: Any = None
    gt: Any = None
    parse_failed: bool = False
    scorable: bool = True
    iou: Optional[float] = None
    abs_error: Optional[float] = None
    parse_strategy: str = ""
    caption: Dict[str, Optional[float]] = field(default_factory=dict)
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "correct": self.correct,
            "parsed": self.parsed,
            "gt": self.gt,
            "parse_failed": self.parse_failed,
            "scorable": self.scorable,
            "iou": self.iou,
            "abs_error": self.abs_error,
            "parse_strategy": self.parse_strategy,
        }
        d.update({k: v for k, v in self.caption.items()})
        d.update(self.extra)
        return d


def score_sample(
    pred_text: str,
    sample: Any,
    thresholds: Sequence[float] = (0.5, 0.7),
    grounding_iou_primary: float = 0.5,
) -> ScoreResult:
    """Score one prediction against one `Sample`.

    Dispatch is on the sample's family, with "has options" taking precedence:
    a counting question delivered as MCQ is scored as MCQ.
    """
    options = list(getattr(sample, "options", []) or [])
    family = str(getattr(sample, "family", "mcq"))
    answer_raw = getattr(sample, "answer_raw", None)
    image_size = getattr(sample, "image_size", None)

    # --- MCQ (covers most of the 16 tasks in the released splits) ----------
    if options:
        gt = gt_letter(answer_raw, options)
        p: MCQParse = parse_mcq(pred_text, options)
        if gt is None:
            return ScoreResult(correct=None, parsed=p.letter, gt=None,
                               parse_failed=not p.ok, scorable=False,
                               parse_strategy=p.strategy)
        return ScoreResult(
            correct=bool(p.letter == gt) if p.ok else False,
            parsed=p.letter, gt=gt, parse_failed=not p.ok, scorable=True,
            parse_strategy=p.strategy,
            extra={"parse_confidence": round(p.confidence, 3)},
        )

    # --- grounding --------------------------------------------------------
    if family.startswith("grounding"):
        g = grounding_score(pred_text, answer_raw, image_size, thresholds)
        key = "acc@{}".format(grounding_iou_primary)
        return ScoreResult(
            correct=g.get(key),
            parsed=parse_bbox(pred_text),
            gt=parse_gt_bbox(answer_raw),
            parse_failed=bool(g.get("parse_failed")),
            scorable=bool(g.get("scorable")),
            iou=g.get("iou"),
            extra={k: v for k, v in g.items()
                   if k.startswith("acc@")},
        )

    # --- captioning -------------------------------------------------------
    if family.startswith("caption"):
        refs = gt_captions(answer_raw)
        cm = caption_metrics(pred_text, refs)
        return ScoreResult(
            correct=None,               # captioning has no accuracy
            parsed=str(pred_text or "").strip()[:4000],
            gt=refs[0][:2000] if refs else None,
            parse_failed=not str(pred_text or "").strip(),
            scorable=bool(refs),
            caption=cm,
        )

    # --- open-ended counting ---------------------------------------------
    if family == "counting":
        pred = parse_count(pred_text)
        gt = gt_count(answer_raw)
        if gt is None:
            return ScoreResult(correct=None, parsed=pred, gt=None,
                               parse_failed=pred is None, scorable=False)
        err = abs(pred - gt) if pred is not None else None
        return ScoreResult(
            correct=bool(pred == gt) if pred is not None else False,
            parsed=pred, gt=gt, parse_failed=pred is None, scorable=True,
            abs_error=float(err) if err is not None else None,
            extra={"within_1": bool(err is not None and err <= 1),
                   "rel_error": (float(err) / gt) if (err is not None and gt) else None},
        )

    # --- open-ended text, no options: exact/containment match -------------
    gt_text = str(answer_raw).strip() if answer_raw is not None else ""
    pred_norm = re.sub(r"\s+", " ", str(pred_text or "")).strip().lower()
    if not gt_text:
        return ScoreResult(correct=None, parsed=pred_norm[:1000], gt=None,
                           parse_failed=not pred_norm, scorable=False)
    return ScoreResult(
        correct=gt_text.lower() in pred_norm,
        parsed=pred_norm[:1000], gt=gt_text[:1000],
        parse_failed=not pred_norm, scorable=True,
    )


# --------------------------------------------------------------------------
# Aggregation helpers
# --------------------------------------------------------------------------

def mean(values: Sequence[Optional[float]]) -> Optional[float]:
    """Mean over non-None values; None when nothing is available.

    Never returns 0.0 for an empty set, which would silently read as a real
    measurement of zero.
    """
    vals = [float(v) for v in values if v is not None]
    return (sum(vals) / len(vals)) if vals else None


def accuracy(correct: Sequence[Optional[bool]]) -> Optional[float]:
    vals = [bool(c) for c in correct if c is not None]
    return (sum(vals) / len(vals)) if vals else None
