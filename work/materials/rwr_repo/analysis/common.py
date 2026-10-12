"""Shared loading and statistics for the Revision-1 analyses.

READ-ONLY with respect to the original experiment: predictions are read from
../Codebase/results/main and nothing there is ever written. All outputs go to
./outputs/ inside this folder.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

try:
    from scipy.stats import binomtest
except Exception:  # pragma: no cover
    binomtest = None

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                     # repository root
RESULTS = ROOT / "results" / "main"
OUT = ROOT / "results" / "analysis_outputs"
OUT.mkdir(exist_ok=True)

METHODS = ["b1_direct", "b2_tiling", "b3_selected", "proposed_ctsr"]
NAME = {"b1_direct": "Direct", "b2_tiling": "Tiling", "b3_selected": "Selection",
        "proposed_ctsr": "Proposed"}
SEED = 20260922
N_BOOT = 10000

# The partition fixed before the experiment (Codebase/ctsr/data/taxonomy.py)
PREREGISTERED_RELATIONAL = {
    "Object Spatial Relationship", "Regional Counting",
    "Counting with Complex Reasoning", "Route Planning",
}
HELD_OUT = {"Counting/Counting with changing detection"}


def _guard_write(path: Path) -> Path:
    path = Path(path).resolve()
    if OUT.resolve() not in path.parents and path != OUT.resolve():
        raise PermissionError(f"Revision1 only writes inside {OUT}; refused {path}")
    return path


def write_json(name: str, obj) -> Path:
    p = _guard_write(OUT / name)
    p.write_text(json.dumps(obj, indent=1, ensure_ascii=False), encoding="utf-8")
    return p


def write_text(name: str, text: str) -> Path:
    p = _guard_write(OUT / name)
    p.write_text(text, encoding="utf-8")
    return p


def load():
    """uid -> record, per method; only items present and scorable in all four."""
    data = {}
    for m in METHODS:
        recs = {}
        with (RESULTS / m / "predictions.jsonl").open(encoding="utf-8") as fh:
            for line in fh:
                if line.strip():
                    r = json.loads(line)
                    recs[r["uid"]] = r
        data[m] = recs
    common = set.intersection(*[set(d) for d in data.values()])
    uids = sorted(u for u in common if all(scorable(data[m][u]) for m in METHODS))
    return data, uids


def scorable(r) -> bool:
    return (r.get("status") == "ok" and r.get("correct") is not None
            and (r.get("artifacts") or {}).get("scorable") is not False)


def correct(data, method, uids):
    return np.array([int(bool(data[method][u]["correct"])) for u in uids], dtype=int)


def mcnemar(a, b, rng, n_boot=N_BOOT):
    """Paired comparison of 0/1 arrays; delta = mean(b) - mean(a)."""
    a, b = np.asarray(a, int), np.asarray(b, int)
    wins = int(((a == 0) & (b == 1)).sum())
    losses = int(((a == 1) & (b == 0)).sum())
    n_disc = wins + losses
    if n_disc == 0:
        p = 1.0
    elif binomtest is not None:
        p = float(binomtest(min(wins, losses), n_disc, 0.5).pvalue)
    else:
        p = min(1.0, 2 * sum(math.comb(n_disc, i) for i in range(min(wins, losses) + 1)) / 2 ** n_disc)
    d = (b - a).astype(float)
    if d.size:
        boots = d[rng.integers(0, d.size, (n_boot, d.size))].mean(1)
        lo, hi = float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))
    else:
        lo = hi = float("nan")
    return {"n": int(a.size), "acc_a": float(a.mean()) if a.size else None,
            "acc_b": float(b.mean()) if b.size else None,
            "delta": float(d.mean()) if d.size else None, "lo": lo, "hi": hi,
            "wins": wins, "losses": losses, "p": p}


def diff_in_diff(d_rel, d_non, rng, n_boot=N_BOOT):
    """Difference between two groups' mean paired differences, bootstrap CI + permutation p."""
    d_rel, d_non = np.asarray(d_rel, float), np.asarray(d_non, float)
    obs = d_rel.mean() - d_non.mean()
    br = d_rel[rng.integers(0, d_rel.size, (n_boot, d_rel.size))].mean(1)
    bn = d_non[rng.integers(0, d_non.size, (n_boot, d_non.size))].mean(1)
    pooled = np.concatenate([d_rel, d_non]).copy()
    perm = np.empty(n_boot)
    for i in range(n_boot):
        rng.shuffle(pooled)
        perm[i] = pooled[:d_rel.size].mean() - pooled[d_rel.size:].mean()
    p = max(float((np.abs(perm) >= abs(obs) - 1e-12).mean()), 1.0 / n_boot)
    return {"did": float(obs), "lo": float(np.percentile(br - bn, 2.5)),
            "hi": float(np.percentile(br - bn, 97.5)), "p_perm": p,
            "p_is_floor": p <= 1.0 / n_boot + 1e-12,
            "d_rel": float(d_rel.mean()), "d_non": float(d_non.mean()),
            "n_rel": int(d_rel.size), "n_non": int(d_non.size)}


def pp(x, nd=1):
    return "--" if x is None or x != x else f"{100 * x:+.{nd}f}"


def pct(x, nd=1):
    return "--" if x is None or x != x else f"{100 * x:.{nd}f}"


def fmt_p(p, floor=False):
    if p is None:
        return "--"
    if floor:
        return "<1e-4"
    return f"{p:.2g}" if p >= 1e-3 else f"{p:.1e}"
