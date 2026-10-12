"""Answer parsing.

Parsing is a measurement instrument, so it must be identical across arms and its
failures must be visible. Two rules:

  1. A parse failure is recorded as `parse_failed=True` and scored as incorrect,
     but is ALSO reported separately. If one arm's prompt is harder to comply
     with, the parse-failure rate will show it, and a difference in accuracy
     driven by format compliance is not a difference in reasoning.

  2. No answer is ever inferred from the options by similarity alone without
     recording that a fallback was used. `parse_mcq` returns the matching
     strategy so the results can be audited.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Any, Dict, List, Optional, Sequence, Tuple

from ..utils.logging_utils import get_logger

LOG = get_logger("ctsr.eval.parsing")

_ANSWER_TAG = re.compile(r"answer\s*[:=]\s*(.+)", re.IGNORECASE)

_NUMBER_WORDS = {
    "zero": 0, "no": 0, "none": 0, "one": 1, "two": 2, "three": 3, "four": 4,
    "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
    "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20,
}


@dataclass
class MCQParse:
    letter: Optional[str]
    index: Optional[int]
    strategy: str      # tagged | bare_letter | exact_text | fuzzy_text | failed
    confidence: float = 1.0

    @property
    def ok(self) -> bool:
        return self.letter is not None


def _after_answer_tag(text: str) -> Optional[str]:
    """Content following the last 'ANSWER:' marker, if any."""
    matches = list(_ANSWER_TAG.finditer(text or ""))
    if not matches:
        return None
    return matches[-1].group(1).strip()


def _norm_text(s: str) -> str:
    s = re.sub(r"[^a-z0-9 ]+", " ", str(s).lower())
    return re.sub(r"\s+", " ", s).strip()


def parse_mcq(text: str, options: Sequence[str],
              fuzzy_threshold: float = 0.82) -> MCQParse:
    """Extract an option choice from a model response.

    Strategies, in order of trust:
      tagged       - a letter directly after 'ANSWER:'
      bare_letter  - a lone letter somewhere in the response
      exact_text   - the response contains an option's text verbatim
      fuzzy_text   - closest option by string similarity, above threshold
    """
    if not options:
        return MCQParse(None, None, "failed", 0.0)
    n = len(options)
    letters = [chr(ord("A") + i) for i in range(n)]
    raw = str(text or "").strip()
    if not raw:
        return MCQParse(None, None, "failed", 0.0)

    # 1) tagged
    tail = _after_answer_tag(raw)
    if tail:
        m = re.match(r"^\W*([A-Za-z])\b", tail)
        if m:
            letter = m.group(1).upper()
            if letter in letters:
                return MCQParse(letter, letters.index(letter), "tagged", 1.0)
        # A tagged full-text answer.
        idx = _match_option_text(tail, options)
        if idx is not None:
            return MCQParse(letters[idx], idx, "exact_text", 0.95)

    # 2) bare letter: prefer an explicitly delimited one, e.g. "(B)" or "B."
    for pattern, conf in (
        (r"\(\s*([A-Za-z])\s*\)", 0.9),
        (r"\b([A-Za-z])\s*[.):]\s", 0.85),
        (r"^\s*([A-Za-z])\s*$", 0.9),
        (r"\boption\s+([A-Za-z])\b", 0.9),
    ):
        for m in re.finditer(pattern, raw, flags=re.IGNORECASE | re.MULTILINE):
            letter = m.group(1).upper()
            if letter in letters:
                return MCQParse(letter, letters.index(letter), "bare_letter", conf)

    # 3) exact option text
    idx = _match_option_text(raw, options)
    if idx is not None:
        return MCQParse(letters[idx], idx, "exact_text", 0.8)

    # 4) fuzzy
    target = _norm_text(tail or raw)
    if target:
        best_i, best_r = None, 0.0
        for i, opt in enumerate(options):
            r = SequenceMatcher(None, target, _norm_text(opt)).ratio()
            if r > best_r:
                best_i, best_r = i, r
        if best_i is not None and best_r >= fuzzy_threshold:
            return MCQParse(letters[best_i], best_i, "fuzzy_text", best_r)

    return MCQParse(None, None, "failed", 0.0)


def _match_option_text(text: str, options: Sequence[str]) -> Optional[int]:
    """Index of the option whose text appears in `text`, longest match wins.

    Longest-first avoids "yes" matching inside "yes, partially" when both are
    options.
    """
    norm = _norm_text(text)
    if not norm:
        return None
    scored: List[Tuple[int, int]] = []
    for i, opt in enumerate(options):
        no = _norm_text(opt)
        if no and no in norm:
            scored.append((len(no), i))
    if not scored:
        return None
    scored.sort(reverse=True)
    return scored[0][1]


def parse_count(text: str) -> Optional[int]:
    """Extract an integer count.

    Prefers the number after 'ANSWER:'; otherwise the last standalone integer,
    since models tend to reason first and conclude last. Number words are
    accepted because small counts are often spelled out.
    """
    raw = str(text or "")
    if not raw.strip():
        return None

    tail = _after_answer_tag(raw)
    for candidate in ([tail] if tail else []) + [raw]:
        if not candidate:
            continue
        nums = re.findall(r"-?\d+", candidate.replace(",", ""))
        if nums:
            try:
                # From a tagged answer take the first number; from free text the last.
                val = int(nums[0] if candidate is tail else nums[-1])
                return max(0, val)
            except ValueError:
                pass
        words = re.findall(r"[a-z]+", candidate.lower())
        for w in words:
            if w in _NUMBER_WORDS:
                return _NUMBER_WORDS[w]
    return None


def parse_bbox(text: str, scale_hint: Optional[str] = None
               ) -> Optional[Tuple[float, float, float, float]]:
    """Extract one bounding box from a response.

    Returns the box in whatever units the model used; the caller converts using
    `coords.norm_to_global` (the grounding prompt requests a 0-1000 grid over the
    whole image). Handles [x1,y1,x2,y2], (x1,y1,x2,y2), JSON, and a bare
    four-number sequence.
    """
    raw = str(text or "")
    if not raw.strip():
        return None

    for candidate in ([_after_answer_tag(raw)] if _after_answer_tag(raw) else []) + [raw]:
        if not candidate:
            continue
        m = re.search(
            r"[\[\(]\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*,\s*"
            r"(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*[\]\)]",
            candidate,
        )
        if m:
            vals = [float(m.group(i)) for i in range(1, 5)]
            return _order_box(vals)
        nums = re.findall(r"-?\d+(?:\.\d+)?", candidate)
        if len(nums) >= 4:
            return _order_box([float(n) for n in nums[:4]])
    return None


def _order_box(vals: Sequence[float]) -> Tuple[float, float, float, float]:
    x1, y1, x2, y2 = [float(v) for v in vals[:4]]
    if x2 < x1:
        x1, x2 = x2, x1
    if y2 < y1:
        y1, y2 = y2, y1
    return (x1, y1, x2, y2)


def parse_gt_bbox(answer_raw: Any) -> Optional[Tuple[float, float, float, float]]:
    """Read a ground-truth box from the dataset's answer field.

    Accepts a list/tuple, a JSON string, or a bracketed string. Returns None when
    the field is not a box - the caller must then treat the sample as unscorable
    rather than scoring it against a guessed value.
    """
    if answer_raw is None:
        return None
    if isinstance(answer_raw, (list, tuple)):
        flat = list(answer_raw)
        # A singleton list wrapping the box.
        if len(flat) == 1 and isinstance(flat[0], (list, tuple)):
            flat = list(flat[0])
        if len(flat) >= 4:
            try:
                return _order_box([float(v) for v in flat[:4]])
            except (TypeError, ValueError):
                return None
        return None
    if isinstance(answer_raw, dict):
        for k in ("bbox", "box", "bbox_2d", "answer"):
            if k in answer_raw:
                return parse_gt_bbox(answer_raw[k])
        return None
    return parse_bbox(str(answer_raw))


def gt_letter(answer_raw: Any, options: Sequence[str]) -> Optional[str]:
    """Normalise a ground-truth MCQ answer to a letter.

    The released answer may be the letter itself or the option text; both are
    handled. Returns None if neither, so the sample is reported unscorable
    instead of being marked wrong.
    """
    if answer_raw is None:
        return None
    s = str(answer_raw).strip()
    if not s:
        return None
    letters = [chr(ord("A") + i) for i in range(len(options))] if options else \
        [chr(ord("A") + i) for i in range(26)]

    m = re.match(r"^\W*([A-Za-z])\W*$", s)
    if m and m.group(1).upper() in letters:
        return m.group(1).upper()
    if options:
        idx = _match_option_text(s, options)
        if idx is not None:
            return chr(ord("A") + idx)
        # Exact normalised equality as a last resort.
        norm = _norm_text(s)
        for i, opt in enumerate(options):
            if _norm_text(opt) == norm:
                return chr(ord("A") + i)
    return None


def gt_count(answer_raw: Any) -> Optional[int]:
    if answer_raw is None:
        return None
    return parse_count(str(answer_raw))


def gt_captions(answer_raw: Any) -> List[str]:
    """Reference caption(s) as a list, since some releases give several."""
    if answer_raw is None:
        return []
    if isinstance(answer_raw, (list, tuple)):
        return [str(a).strip() for a in answer_raw if str(a).strip()]
    s = str(answer_raw).strip()
    return [s] if s else []
