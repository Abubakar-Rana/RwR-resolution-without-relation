"""Statistical tests for the controlled comparison.

The study's whole claim is a difference between two arms on the same samples
(Baseline 3 vs Proposed), so every test here is PAIRED. Pairing is done on uid,
and a sample is used only if both arms produced a scorable result for it - an
unpaired comparison across different sample subsets would be invalid, and this
module refuses to make one silently (it reports how many samples were dropped).

Implemented:
  bootstrap_ci            percentile CI for a single metric
  paired_bootstrap_delta  CI and p-value for the difference between two arms
  mcnemar                 exact binomial test for paired binary outcomes
  paired_permutation      exact/Monte-Carlo sign-flip test for paired continuous
  holm_bonferroni         multiple-comparison correction across tasks

scipy is used when present (exact binomial), with a pure-Python fallback so no
result is lost to a missing dependency. Everything is seeded.

On multiple comparisons: the plan tests 16 tasks plus two groups. Reporting 18
uncorrected p-values would guarantee false positives, so `holm_bonferroni` should
be applied to the per-task family, while the two pre-registered group-level tests
(relational, non-relational) are the primary confirmatory analysis.
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

from ..utils.logging_utils import get_logger

LOG = get_logger("ctsr.eval.stats")


# --------------------------------------------------------------------------
# Single-sample CI
# --------------------------------------------------------------------------

@dataclass
class Estimate:
    value: Optional[float]
    lo: Optional[float] = None
    hi: Optional[float] = None
    n: int = 0
    method: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "value": _r(self.value),
            "ci_lo": _r(self.lo),
            "ci_hi": _r(self.hi),
            "n": self.n,
            "method": self.method,
        }

    def __str__(self) -> str:
        if self.value is None:
            return "n/a"
        if self.lo is None:
            return "{:.4f}".format(self.value)
        return "{:.4f} [{:.4f}, {:.4f}]".format(self.value, self.lo, self.hi)


def _r(v: Optional[float], nd: int = 6) -> Optional[float]:
    return None if v is None else round(float(v), nd)


def bootstrap_ci(
    values: Sequence[float],
    statistic: Callable[[Sequence[float]], float] = None,
    n_boot: int = 10000,
    alpha: float = 0.05,
    seed: int = 1234,
) -> Estimate:
    """Percentile bootstrap CI for a statistic of one sample."""
    vals = [float(v) for v in values if v is not None]
    if not vals:
        return Estimate(None, None, None, 0, "bootstrap(empty)")
    stat = statistic or (lambda xs: sum(xs) / len(xs))
    point = float(stat(vals))
    if len(vals) < 2:
        return Estimate(point, None, None, len(vals), "bootstrap(n<2)")

    rng = random.Random(seed)
    n = len(vals)
    boots: List[float] = []
    for _ in range(int(n_boot)):
        sample = [vals[rng.randrange(n)] for _ in range(n)]
        try:
            boots.append(float(stat(sample)))
        except Exception:
            continue
    if not boots:
        return Estimate(point, None, None, n, "bootstrap(failed)")
    boots.sort()
    lo = boots[max(0, int(math.floor((alpha / 2) * len(boots))))]
    hi = boots[min(len(boots) - 1, int(math.ceil((1 - alpha / 2) * len(boots))) - 1)]
    return Estimate(point, lo, hi, n, "percentile_bootstrap(n_boot={})".format(n_boot))


# --------------------------------------------------------------------------
# Paired comparisons
# --------------------------------------------------------------------------

@dataclass
class PairedResult:
    n_pairs: int = 0
    n_dropped: int = 0
    mean_a: Optional[float] = None
    mean_b: Optional[float] = None
    delta: Optional[float] = None
    ci_lo: Optional[float] = None
    ci_hi: Optional[float] = None
    p_value: Optional[float] = None
    test: str = ""
    detail: Dict[str, Any] = field(default_factory=dict)

    @property
    def significant_05(self) -> Optional[bool]:
        return None if self.p_value is None else bool(self.p_value < 0.05)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "n_pairs": self.n_pairs,
            "n_dropped": self.n_dropped,
            "mean_a": _r(self.mean_a),
            "mean_b": _r(self.mean_b),
            "delta": _r(self.delta),
            "ci_lo": _r(self.ci_lo),
            "ci_hi": _r(self.ci_hi),
            "p_value": _r(self.p_value, 8),
            "test": self.test,
            "significant_05": self.significant_05,
            **self.detail,
        }


def align_pairs(
    a: Dict[str, Optional[float]],
    b: Dict[str, Optional[float]],
) -> Tuple[List[float], List[float], List[str], int]:
    """Intersect two uid->value maps, dropping any uid missing/None in either.

    Returns (values_a, values_b, uids, n_dropped). Dropping is symmetric, which is
    what keeps the comparison paired.
    """
    uids = sorted(set(a) & set(b))
    va: List[float] = []
    vb: List[float] = []
    kept: List[str] = []
    dropped = 0
    for u in uids:
        x, y = a.get(u), b.get(u)
        if x is None or y is None:
            dropped += 1
            continue
        va.append(float(x))
        vb.append(float(y))
        kept.append(u)
    dropped += len(set(a) ^ set(b))
    return va, vb, kept, dropped


def paired_bootstrap_delta(
    a: Dict[str, Optional[float]],
    b: Dict[str, Optional[float]],
    n_boot: int = 10000,
    alpha: float = 0.05,
    seed: int = 1234,
) -> PairedResult:
    """Bootstrap CI and two-sided p-value for mean(b) - mean(a) on paired data.

    Resamples PAIRS (not values independently), which is what preserves the
    correlation between arms and gives the narrower, correct interval.

    The p-value is the bootstrap proportion of resamples whose delta falls on the
    other side of zero, doubled; it is floored at 1/n_boot since a bootstrap
    cannot resolve a p-value below its own resolution.
    """
    va, vb, kept, dropped = align_pairs(a, b)
    res = PairedResult(n_pairs=len(kept), n_dropped=dropped,
                       test="paired_bootstrap(n_boot={})".format(n_boot))
    if not kept:
        LOG.warning("paired_bootstrap_delta: no overlapping scorable samples.")
        return res

    res.mean_a = sum(va) / len(va)
    res.mean_b = sum(vb) / len(vb)
    res.delta = res.mean_b - res.mean_a
    if len(kept) < 2:
        return res

    diffs = [vb[i] - va[i] for i in range(len(kept))]
    rng = random.Random(seed)
    n = len(diffs)
    boots: List[float] = []
    for _ in range(int(n_boot)):
        s = 0.0
        for _ in range(n):
            s += diffs[rng.randrange(n)]
        boots.append(s / n)
    boots.sort()
    res.ci_lo = boots[max(0, int(math.floor((alpha / 2) * len(boots))))]
    res.ci_hi = boots[min(len(boots) - 1, int(math.ceil((1 - alpha / 2) * len(boots))) - 1)]

    n_le = sum(1 for d in boots if d <= 0.0)
    n_ge = sum(1 for d in boots if d >= 0.0)
    p = 2.0 * min(n_le, n_ge) / len(boots)
    res.p_value = max(min(1.0, p), 1.0 / len(boots))
    res.detail["mean_paired_diff"] = _r(sum(diffs) / n)
    res.detail["n_improved"] = sum(1 for d in diffs if d > 0)
    res.detail["n_worsened"] = sum(1 for d in diffs if d < 0)
    res.detail["n_tied"] = sum(1 for d in diffs if d == 0)
    return res


def mcnemar(
    a: Dict[str, Optional[bool]],
    b: Dict[str, Optional[bool]],
    exact: bool = True,
    continuity_correction: bool = True,
) -> PairedResult:
    """McNemar's test for paired binary outcomes (the right test for accuracy).

    Only the discordant pairs carry information:
      b01 = a wrong, b right   (the proposed method's wins)
      b10 = a right, b wrong   (its losses)

    Exact two-sided binomial test by default; the chi-square approximation with
    continuity correction is used when `exact=False`, and is unreliable when
    b01+b10 < 25, so we fall back to exact in that case regardless.
    """
    aa = {k: (None if v is None else bool(v)) for k, v in a.items()}
    bb = {k: (None if v is None else bool(v)) for k, v in b.items()}
    uids = sorted(set(aa) & set(bb))
    kept = [u for u in uids if aa.get(u) is not None and bb.get(u) is not None]
    dropped = (len(set(aa) ^ set(bb))
               + sum(1 for u in uids if aa.get(u) is None or bb.get(u) is None))

    res = PairedResult(n_pairs=len(kept), n_dropped=dropped, test="mcnemar")
    if not kept:
        LOG.warning("mcnemar: no overlapping scorable samples.")
        return res

    b01 = sum(1 for u in kept if (not aa[u]) and bb[u])
    b10 = sum(1 for u in kept if aa[u] and (not bb[u]))
    b11 = sum(1 for u in kept if aa[u] and bb[u])
    b00 = sum(1 for u in kept if (not aa[u]) and (not bb[u]))

    res.mean_a = sum(1 for u in kept if aa[u]) / len(kept)
    res.mean_b = sum(1 for u in kept if bb[u]) / len(kept)
    res.delta = res.mean_b - res.mean_a
    res.detail.update({"b01_only_b_correct": b01, "b10_only_a_correct": b10,
                       "b11_both_correct": b11, "b00_both_wrong": b00})

    n_disc = b01 + b10
    if n_disc == 0:
        res.p_value = 1.0
        res.test = "mcnemar(no_discordant_pairs)"
        return res

    use_exact = exact or n_disc < 25
    if use_exact:
        res.p_value = _exact_binomial_two_sided(min(b01, b10), n_disc)
        res.test = "mcnemar_exact"
    else:
        num = (abs(b01 - b10) - 1.0) ** 2 if continuity_correction else (b01 - b10) ** 2
        chi2 = num / n_disc
        res.p_value = _chi2_sf_1df(chi2)
        res.test = "mcnemar_chi2"
        res.detail["chi2"] = _r(chi2)

    # Wilson-style CI on the difference of correlated proportions, via the
    # bootstrap over pairs (simple and assumption-light).
    boot = paired_bootstrap_delta(
        {u: (1.0 if aa[u] else 0.0) for u in kept},
        {u: (1.0 if bb[u] else 0.0) for u in kept},
    )
    res.ci_lo, res.ci_hi = boot.ci_lo, boot.ci_hi
    return res


def _exact_binomial_two_sided(k: int, n: int, p: float = 0.5) -> float:
    """Two-sided exact binomial p-value. Uses scipy when available."""
    try:
        from scipy.stats import binomtest
        return float(binomtest(k, n, p, alternative="two-sided").pvalue)
    except Exception:
        pass
    try:
        from scipy.stats import binom_test  # older scipy
        return float(binom_test(k, n, p, alternative="two-sided"))
    except Exception:
        pass
    # Pure-python: for p=0.5 the distribution is symmetric, so doubling the
    # lower tail is exact (capped at 1).
    if n <= 0:
        return 1.0
    tail = sum(math.comb(n, i) for i in range(0, k + 1)) / (2.0 ** n)
    return float(min(1.0, 2.0 * tail))


def _chi2_sf_1df(x: float) -> float:
    """Survival function of chi-square with 1 df = erfc(sqrt(x/2))."""
    if x <= 0:
        return 1.0
    return float(math.erfc(math.sqrt(x / 2.0)))


def paired_permutation(
    a: Dict[str, Optional[float]],
    b: Dict[str, Optional[float]],
    n_perm: int = 10000,
    seed: int = 1234,
) -> PairedResult:
    """Sign-flip permutation test on paired differences.

    Assumption-light alternative to a paired t-test, appropriate for the bounded,
    non-normal metrics here (IoU, BLEU). Enumerates exactly when 2^n <= n_perm.
    """
    va, vb, kept, dropped = align_pairs(a, b)
    res = PairedResult(n_pairs=len(kept), n_dropped=dropped, test="paired_permutation")
    if not kept:
        return res
    res.mean_a = sum(va) / len(va)
    res.mean_b = sum(vb) / len(vb)
    res.delta = res.mean_b - res.mean_a

    diffs = [vb[i] - va[i] for i in range(len(kept))]
    nz = [d for d in diffs if d != 0.0]
    if not nz:
        res.p_value = 1.0
        res.test = "paired_permutation(all_ties)"
        return res

    observed = abs(sum(diffs) / len(diffs))
    n = len(diffs)

    if n <= 20 and (2 ** n) <= n_perm:
        count = 0
        total = 2 ** n
        for mask in range(total):
            s = 0.0
            for i in range(n):
                s += diffs[i] if (mask >> i) & 1 else -diffs[i]
            if abs(s / n) >= observed - 1e-15:
                count += 1
        res.p_value = count / total
        res.test = "paired_permutation_exact"
        return res

    rng = random.Random(seed)
    count = 0
    for _ in range(int(n_perm)):
        s = 0.0
        for d in diffs:
            s += d if rng.random() < 0.5 else -d
        if abs(s / n) >= observed - 1e-15:
            count += 1
    res.p_value = max((count + 1) / (n_perm + 1), 1.0 / (n_perm + 1))
    res.test = "paired_permutation_mc(n_perm={})".format(n_perm)
    return res


# --------------------------------------------------------------------------
# Multiple comparisons
# --------------------------------------------------------------------------

def holm_bonferroni(p_values: Dict[str, Optional[float]],
                    alpha: float = 0.05) -> Dict[str, Dict[str, Any]]:
    """Holm-Bonferroni step-down correction.

    Returns per-key adjusted p-value and reject decision. Keys whose p-value is
    None are excluded from the family (they contribute no test) and marked
    accordingly, rather than being counted as non-significant tests that inflate
    the correction.
    """
    valid = {k: float(v) for k, v in p_values.items() if v is not None}
    out: Dict[str, Dict[str, Any]] = {
        k: {"p_value": None, "p_adjusted": None, "reject": None,
            "note": "no test (metric unavailable)"}
        for k, v in p_values.items() if v is None
    }
    if not valid:
        return out

    ordered = sorted(valid.items(), key=lambda kv: kv[1])
    m = len(ordered)
    running = 0.0
    for i, (key, p) in enumerate(ordered):
        adj = min(1.0, (m - i) * p)
        # Enforce monotonicity of adjusted p-values.
        running = max(running, adj)
        out[key] = {
            "p_value": _r(p, 8),
            "p_adjusted": _r(running, 8),
            "reject": bool(running < alpha),
            "rank": i + 1,
            "family_size": m,
        }
    return out


def compare_arms(
    per_sample_a: Dict[str, Any],
    per_sample_b: Dict[str, Any],
    metric: str = "correct",
    n_boot: int = 10000,
    seed: int = 1234,
) -> PairedResult:
    """Pick the right paired test for a metric and run it.

    Binary metrics ("correct") -> McNemar. Continuous metrics -> paired bootstrap
    plus a permutation p-value, since the bootstrap p-value is less reliable in
    the tails for small n.
    """
    if metric == "correct":
        return mcnemar(per_sample_a, per_sample_b)
    res = paired_bootstrap_delta(per_sample_a, per_sample_b, n_boot=n_boot, seed=seed)
    perm = paired_permutation(per_sample_a, per_sample_b, seed=seed)
    if perm.p_value is not None:
        res.p_value = perm.p_value
        res.test = "{} + {}".format(res.test, perm.test)
    return res
