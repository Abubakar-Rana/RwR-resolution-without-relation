#!/usr/bin/env python
"""Tier-2 experiment: do explicit relations help once objects are actually found?

The original run used the VLM itself as the object extractor, and it returned no objects on
66% of scenes, so the relation block was usually empty. This script replaces ONLY that step
with a dedicated open-vocabulary detector (Grounding DINO) and re-runs two methods:

    sel_det   Selection  + detector objects        (no relation block)
    prop_det  Proposed   + detector objects        (with relation block)

Everything else is held fixed:
  * the SAME 5 tiles per item, replayed from results/main/b3_selected (not re-scored)
  * the same Qwen2.5-VL model, config, overview, crops, prompts and final call

The key comparison is prop_det vs sel_det (the relation block, with working grounding).

USAGE (from the repository root, next to configs/ and ctsr/):

    python scripts/06_detector_grounding.py --check        # 1-2 min: loads everything, 2 items
    python scripts/06_detector_grounding.py                # full run (resumable; ~4 GPU-hours)
    python scripts/06_detector_grounding.py --analyze-only # re-make the summary

Writes ONLY to results/detector_grounding/ . Never modifies results/main/.
"""
from __future__ import annotations

import argparse
import inspect
import json
import math
import random
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent          # repo root
sys.path.insert(0, str(HERE))

from ctsr.config import build_backend, load_config, load_samples  # noqa: E402
from ctsr.data.schema import DetectedObject  # noqa: E402
from ctsr.models.detector import ExtractionResult, RegionProposer  # noqa: E402
from ctsr.pipelines.hierarchical import HierarchicalPipeline  # noqa: E402
from ctsr.pipelines.runner import run_experiment  # noqa: E402
from ctsr.spatial.coords import lift_to_global, touches_tile_border  # noqa: E402
from ctsr.tiling.selection import TileScore, TileScorer  # noqa: E402
from ctsr.utils.io_utils import atomic_write_json, ensure_dir, load_jsonl  # noqa: E402
from ctsr.utils.logging_utils import get_logger  # noqa: E402
from ctsr.utils.seed import set_seed  # noqa: E402

LOG = get_logger("tier2")

RELATIONAL = {"Object Spatial Relationship", "Regional Counting",
              "Counting with Complex Reasoning", "Route Planning"}
HELD_OUT = {"Counting/Counting with changing detection"}

# Generic remote-sensing vocabulary, always included in the detector prompt so that
# questions with few content words still get common objects detected.
DEFAULT_CLASSES = [
    "building", "house", "road", "car", "vehicle", "truck", "ship", "boat", "airplane",
    "storage tank", "bridge", "tree", "water", "river", "lake", "field", "farmland",
    "parking lot", "stadium", "sports field", "swimming pool", "roundabout", "greenhouse",
]


# ---------------------------------------------------------------------------
# 1. Replay the original tile selection exactly
# ---------------------------------------------------------------------------
class FixedSelectionScorer(TileScorer):
    """Scores the tiles chosen in the original run highest, in their original order.

    With spatial diversity switched off in the pipeline, select_tiles() then returns
    exactly the original tiles, so the only thing that changes is object extraction.
    """
    name = "fixed_from_original_run"

    def __init__(self, chosen):            # chosen[(uid, image_index)] -> [tile ids]
        self.chosen = chosen
        self.current_uid = None
        self.n_missing = 0

    def score(self, ti, tiles, question, options=None, meter=None):
        order = self.chosen.get((self.current_uid, ti.image_index))
        if order is None:
            self.n_missing += 1
            raise KeyError(f"no original selection for {self.current_uid} image {ti.image_index}")
        rank = {tid: len(order) - i for i, tid in enumerate(order)}
        return [TileScore(tile_id=t.tile_id, score=float(rank.get(t.tile_id, 0)),
                          components={"replayed": float(t.tile_id in rank)}) for t in tiles]

    def describe(self):
        return {"scorer": self.name}


class ReplayPipeline(HierarchicalPipeline):
    """HierarchicalPipeline that tells the replay scorer which item it is on."""

    def run_sample(self, sample):
        self.scorer.current_uid = sample.uid
        return super().run_sample(sample)


# ---------------------------------------------------------------------------
# 2. The detector
# ---------------------------------------------------------------------------
class GroundingDinoProposer(RegionProposer):
    """Open-vocabulary detector used in place of VLM extraction, one pass per tile."""
    name = "grounding_dino"
    uses_vlm = False

    def __init__(self, model_id, box_threshold=0.30, text_threshold=0.25,
                 max_objects_per_tile=24, device=None):
        self.model_id = model_id
        self.box_threshold = float(box_threshold)
        self.text_threshold = float(text_threshold)
        self.max_objects_per_tile = int(max_objects_per_tile)
        self.device = device
        self._model = self._proc = None
        self._post_kw = None

    def load(self):
        if self._model is not None:
            return self
        import torch
        from transformers import AutoModelForZeroShotObjectDetection, AutoProcessor
        self.device = self.device or ("cuda" if torch.cuda.is_available() else "cpu")
        LOG.info("Loading detector %s on %s", self.model_id, self.device)
        self._proc = AutoProcessor.from_pretrained(self.model_id)
        self._model = AutoModelForZeroShotObjectDetection.from_pretrained(self.model_id)
        self._model.to(self.device).eval()
        sig = inspect.signature(self._proc.post_process_grounded_object_detection).parameters
        # transformers renamed box_threshold -> threshold; support both
        self._post_kw = "threshold" if "threshold" in sig else "box_threshold"
        return self

    @staticmethod
    def prompt(keywords):
        phrases, seen = [], set()
        for w in list(keywords or [])[:10] + DEFAULT_CLASSES:
            w = str(w).lower().strip(" .")
            if w and w not in seen:
                seen.add(w)
                phrases.append(w)
        return ". ".join(phrases[:30]) + "."

    def extract(self, ti, tiles, question, keywords=None, meter=None, collector=None):
        import torch
        self.load()
        res = ExtractionResult()
        size = (ti.width, ti.height)
        text = self.prompt(keywords)
        for tile in tiles:
            try:
                crop = ti.crop(tile)
                inputs = self._proc(images=crop, text=text, return_tensors="pt").to(self.device)
                with torch.inference_mode():
                    out = self._model(**inputs)
                kw = {self._post_kw: self.box_threshold, "text_threshold": self.text_threshold,
                      "target_sizes": [crop.size[::-1]]}
                det = self._proc.post_process_grounded_object_detection(
                    out, inputs["input_ids"], **kw)[0]
            except Exception as exc:
                res.n_tiles_failed += 1
                if collector is not None:
                    collector.add(f"detector:tile{tile.tile_id}", exc)
                LOG.error("detector failed on tile %s: %s", tile.tile_id, exc)
                continue
            res.n_tiles_processed += 1
            boxes = det.get("boxes")
            scores = det.get("scores")
            labels = det.get("text_labels") or det.get("labels") or []
            n = 0 if boxes is None else len(boxes)
            res.n_raw += n
            order = sorted(range(n), key=lambda i: -float(scores[i])) if n else []
            for i in order[:self.max_objects_per_tile]:
                box = [float(v) for v in boxes[i].tolist()]
                g = lift_to_global(tuple(box), tile, crop_size=crop.size, clamp=True, image_size=size)
                if g is None:
                    res.n_parse_failed += 1
                    continue
                lab = labels[i] if i < len(labels) and isinstance(labels[i], str) else "object"
                obj = DetectedObject(label=lab.strip() or "object", bbox_global=g,
                                     score=float(scores[i]), tile_id=tile.tile_id)
                if touches_tile_border(g, tile):
                    obj.attributes["border"] = True
                    res.n_border_touching += 1
                res.objects.append(obj)
        return res

    def describe(self):
        return {"proposer": self.name, "model_id": self.model_id,
                "box_threshold": self.box_threshold, "text_threshold": self.text_threshold,
                "max_objects_per_tile": self.max_objects_per_tile}


class StubDetector(RegionProposer):
    """Plumbing test only: deterministic fake boxes. Never used for results."""
    name = "stub_detector"
    uses_vlm = False

    def extract(self, ti, tiles, question, keywords=None, meter=None, collector=None):
        res = ExtractionResult()
        rng = random.Random(hash(question) & 0xFFFF)
        for tile in tiles:
            res.n_tiles_processed += 1
            for _ in range(4):
                x, y = rng.uniform(0, tile.width - 80), rng.uniform(0, tile.height - 80)
                g = lift_to_global((x, y, x + 60, y + 60), tile, crop_size=(tile.width, tile.height),
                                   clamp=True, image_size=(ti.width, ti.height))
                res.objects.append(DetectedObject("building", g, 0.9, tile_id=tile.tile_id))
                res.n_raw += 1
        return res


# ---------------------------------------------------------------------------
# 3. Item subset
# ---------------------------------------------------------------------------
def load_original(orig_dir):
    out = {}
    for arm in ("b1_direct", "b2_tiling", "b3_selected", "proposed_ctsr"):
        p = Path(orig_dir) / arm / "predictions.jsonl"
        if p.exists():
            out[arm] = {r["uid"]: r for r in load_jsonl(p) if r.get("uid")}
    if "b3_selected" not in out:
        raise FileNotFoundError(f"{orig_dir}/b3_selected/predictions.jsonl is required "
                                "(its tile selections are replayed)")
    return out


def choose_subset(orig, n_nonrel, seed, use_all):
    b3 = orig["b3_selected"]
    ok = [u for u, r in b3.items() if r.get("status") == "ok" and r.get("correct") is not None]
    if use_all:
        return sorted(ok)
    rel = sorted(u for u in ok if b3[u]["task"] in RELATIONAL)
    non = [u for u in ok if b3[u]["task"] not in RELATIONAL and b3[u]["task"] not in HELD_OUT]
    by_task = defaultdict(list)
    for u in sorted(non):
        by_task[b3[u]["task"]].append(u)
    rng = random.Random(seed)
    picked = []
    total = len(non)
    for t, us in sorted(by_task.items()):                 # proportional, per task
        k = max(1, round(n_nonrel * len(us) / total)) if total else 0
        rng.shuffle(us)
        picked += us[:k]
    return sorted(rel + picked)


def chosen_map(orig):
    m = {}
    for uid, r in orig["b3_selected"].items():
        for sel in (r.get("artifacts") or {}).get("selection") or []:
            m[(uid, int(sel.get("image_index", 0)))] = list(sel.get("chosen") or [])
    return m


# ---------------------------------------------------------------------------
# 4. Analysis
# ---------------------------------------------------------------------------
def mcnemar(a, b, rng, n_boot=10000):
    wins = sum(1 for x, y in zip(a, b) if x == 0 and y == 1)
    losses = sum(1 for x, y in zip(a, b) if x == 1 and y == 0)
    n = len(a)
    if n == 0:
        return None
    try:
        from scipy.stats import binomtest
        p = float(binomtest(min(wins, losses), wins + losses, 0.5).pvalue) if wins + losses else 1.0
    except Exception:
        k, m = min(wins, losses), wins + losses
        p = min(1.0, 2 * sum(math.comb(m, i) for i in range(k + 1)) / 2 ** m) if m else 1.0
    import numpy as np
    d = np.asarray([y - x for x, y in zip(a, b)], float)
    gen = np.random.default_rng(rng.randrange(2 ** 31))
    boots = d[gen.integers(0, n, (n_boot, n))].mean(1)
    return {"n": n, "acc_a": sum(a) / n, "acc_b": sum(b) / n, "delta": float(d.mean()),
            "lo": float(np.percentile(boots, 2.5)), "hi": float(np.percentile(boots, 97.5)),
            "wins": wins, "losses": losses, "p": p, "mde80": 2.801585 * float(boots.std())}


def analyze(out_dir, orig_dir, n_boot=10000):
    rng = random.Random(20260922)
    orig = load_original(orig_dir)
    new = {}
    for arm in ("sel_det", "prop_det"):
        p = Path(out_dir) / arm / "predictions.jsonl"
        if p.exists():
            new[arm] = {r["uid"]: r for r in load_jsonl(p) if r.get("uid")}
    if len(new) < 2:
        LOG.error("Need both sel_det and prop_det predictions in %s", out_dir)
        return None
    arms = {"Direct": orig.get("b1_direct"), "Selection (VLM extractor)": orig["b3_selected"],
            "Proposed (VLM extractor)": orig.get("proposed_ctsr"),
            "Selection + detector": new["sel_det"], "Proposed + detector": new["prop_det"]}

    def good(r):
        return r and r.get("status") == "ok" and r.get("correct") is not None

    uids = sorted(u for u in new["prop_det"]
                  if all(good((a or {}).get(u)) for a in arms.values() if a is not None))
    task = {u: orig["b3_selected"][u]["task"] for u in uids}
    grp = {u: "relational" if task[u] in RELATIONAL else
           ("held-out" if task[u] in HELD_OUT else "non-relational") for u in uids}

    def acc(arm, us):
        return sum(int(bool(arms[arm][u]["correct"])) for u in us) / len(us) if us else None

    def vec(arm, us):
        return [int(bool(arms[arm][u]["correct"])) for u in us]

    groups = {"all": uids, "relational": [u for u in uids if grp[u] == "relational"],
              "non-relational": [u for u in uids if grp[u] == "non-relational"]}
    summary = {"n_items": len(uids), "groups": {g: len(v) for g, v in groups.items()},
               "accuracy": {a: {g: acc(a, us) for g, us in groups.items()}
                            for a, r in arms.items() if r is not None}}

    def zero_rate(recs, us):
        return sum(1 for u in us if (recs[u].get("n_objects") or 0) == 0) / len(us) if us else None

    def rel_stats(recs, us):
        nr = [((recs[u].get("artifacts") or {}).get("n_relations_built") or 0) for u in us]
        nc = [(((recs[u].get("artifacts") or {}).get("graph_stats") or {}).get("n_cross_tile") or 0)
              for u in us]
        return {"zero_object_rate": zero_rate(recs, us),
                "mean_objects": sum((recs[u].get("n_objects") or 0) for u in us) / len(us),
                "share_with_relations": sum(1 for x in nr if x > 0) / len(us),
                "share_with_cross_tile": sum(1 for x in nc if x > 0) / len(us)}

    summary["grounding"] = {
        "VLM extractor (original Proposed)": rel_stats(orig["proposed_ctsr"], uids),
        "detector (Proposed + detector)": rel_stats(new["prop_det"], uids)}

    comps = {
        "relation block, with detector (Selection+det -> Proposed+det)  [KEY TEST]":
            ("Selection + detector", "Proposed + detector"),
        "relation block, original (Selection -> Proposed)":
            ("Selection (VLM extractor)", "Proposed (VLM extractor)"),
        "detector objects vs VLM objects, no relations":
            ("Selection (VLM extractor)", "Selection + detector"),
        "full new method vs original Proposed":
            ("Proposed (VLM extractor)", "Proposed + detector"),
        "full new method vs Direct":
            ("Direct", "Proposed + detector"),
    }
    summary["comparisons"] = {}
    for name, (a, b) in comps.items():
        if arms.get(a) is None:
            continue
        summary["comparisons"][name] = {g: mcnemar(vec(a, us), vec(b, us), rng, n_boot)
                                        for g, us in groups.items()}

    # key test restricted to items where the detector actually produced relations
    P = new["prop_det"]
    has_rel = [u for u in uids if ((P[u].get("artifacts") or {}).get("n_relations_built") or 0) > 0]
    has_x = [u for u in uids if (((P[u].get("artifacts") or {}).get("graph_stats") or {})
                                 .get("n_cross_tile") or 0) > 0]
    summary["key_test_by_stratum"] = {}
    for sname, su in (("relation block non-empty", has_rel), (">=1 cross-tile relation", has_x)):
        for g in ("relational", "non-relational"):
            us = [u for u in su if grp[u] == g]
            summary["key_test_by_stratum"][f"{sname} / {g}"] = mcnemar(
                vec("Selection + detector", us), vec("Proposed + detector", us), rng, n_boot)

    comp = {}
    for arm in ("sel_det", "prop_det"):
        cs = [(new[arm][u].get("compute") or {}) for u in uids]
        comp[arm] = {"calls": sum(c.get("n_vlm_calls") or 0 for c in cs) / len(cs),
                     "seconds": sum(c.get("wall_seconds") or 0 for c in cs) / len(cs),
                     "gpu_hours": sum(c.get("wall_seconds") or 0 for c in cs) / 3600}
    summary["compute"] = comp
    atomic_write_json(Path(out_dir) / "summary.json", summary)

    def fp(x):
        return "--" if x is None else f"{100 * x:+.1f}"

    lines = [f"# Tier-2 detector experiment: {len(uids)} items "
             f"({summary['groups']['relational']} relational, "
             f"{summary['groups']['non-relational']} non-relational)", "",
             "## Accuracy (%)", "", "| Method | All | Relational | Non-relational |", "|---|---|---|---|"]
    for a, v in summary["accuracy"].items():
        lines.append(f"| {a} | {100 * v['all']:.1f} | {100 * (v['relational'] or 0):.1f} | "
                     f"{100 * (v['non-relational'] or 0):.1f} |")
    lines += ["", "## Grounding", "", "| Extractor | no-object scenes | mean objects | with relations | with cross-tile |",
              "|---|---|---|---|---|"]
    for k, v in summary["grounding"].items():
        lines.append(f"| {k} | {100 * v['zero_object_rate']:.0f}% | {v['mean_objects']:.1f} | "
                     f"{100 * v['share_with_relations']:.0f}% | {100 * v['share_with_cross_tile']:.0f}% |")
    lines += ["", "## Paired comparisons (pp, 95% CI, McNemar p, MDE at 80% power)", ""]
    for name, byg in summary["comparisons"].items():
        lines.append(f"**{name}**")
        for g, r in byg.items():
            if r:
                lines.append(f"- {g}: {fp(r['delta'])} [{fp(r['lo'])}, {fp(r['hi'])}], "
                             f"p={r['p']:.3g}, wins/losses {r['wins']}/{r['losses']}, "
                             f"MDE {100 * r['mde80']:.1f} (n={r['n']})")
        lines.append("")
    lines += ["## Key test by stratum (post-treatment; descriptive)", ""]
    for k, r in summary["key_test_by_stratum"].items():
        if r:
            lines.append(f"- {k}: {fp(r['delta'])} [{fp(r['lo'])}, {fp(r['hi'])}], p={r['p']:.3g}, n={r['n']}")
    lines += ["", "## Compute", ""] + [f"- {a}: {v['calls']:.2f} VLM calls/item, {v['seconds']:.1f} s/item, "
                                       f"{v['gpu_hours']:.1f} GPU-h" for a, v in comp.items()]
    (Path(out_dir) / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return summary


# ---------------------------------------------------------------------------
# 5. Main
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", default="configs/main.yaml")
    ap.add_argument("--set", dest="overrides", action="append", default=[])
    ap.add_argument("--orig-results", default="results/main",
                    help="the original run (read-only); its tile selections are replayed")
    ap.add_argument("--out", default="results/detector_grounding")
    ap.add_argument("--detector", default="IDEA-Research/grounding-dino-base")
    ap.add_argument("--box-threshold", type=float, default=0.30)
    ap.add_argument("--text-threshold", type=float, default=0.25)
    ap.add_argument("--n-nonrel", type=int, default=400,
                    help="stratified non-relational sample size (all relational items are used)")
    ap.add_argument("--all", action="store_true", help="run every scored item instead of the subset")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--check", action="store_true", help="quick preflight on 2 items, then stop")
    ap.add_argument("--analyze-only", action="store_true")
    ap.add_argument("--stub", action="store_true",
                    help="plumbing test with fake VLM and fake detector (no GPU, no results)")
    args = ap.parse_args()

    out = Path(args.out).resolve()
    if out == Path(args.orig_results).resolve() or Path(args.orig_results).resolve() in out.parents:
        sys.exit("--out must be outside the original results folder")
    ensure_dir(out)
    get_logger("tier2", logfile=out / "tier2.log")

    if args.analyze_only:
        analyze(out, args.orig_results)
        return

    overrides = list(args.overrides)
    if args.stub:
        overrides.append("model.backend=stub")
    cfg = load_config(args.config, overrides)
    cfg.setdefault("tier2", {}).update({"detector": args.detector, "box_threshold": args.box_threshold,
                                        "text_threshold": args.text_threshold,
                                        "orig_results": str(args.orig_results)})
    set_seed(int(cfg.get("seed", 1234)))

    orig = load_original(args.orig_results)
    subset = set(choose_subset(orig, args.n_nonrel, int(cfg.get("seed", 1234)), args.all))
    LOG.info("Subset: %d items", len(subset))

    samples, info = load_samples(cfg)
    samples = [s for s in samples if s.uid in subset]
    missing = len(subset) - len(samples)
    if missing:
        LOG.warning("%d subset items were not found in the loaded dataset (uid mismatch?)", missing)
    if not samples:
        sys.exit("No samples matched the original run's uids. Is --config the one used for results/main?")
    if args.check:
        samples = samples[:2]
    elif args.limit:
        samples = samples[:args.limit]

    backend = build_backend(cfg)
    backend.load()
    detector = StubDetector() if args.stub else GroundingDinoProposer(
        args.detector, args.box_threshold, args.text_threshold)
    if not args.stub:
        detector.load()
    scorer = FixedSelectionScorer(chosen_map(orig))

    t0 = time.time()
    for arm, use_rel in (("sel_det", False), ("prop_det", True)):
        pipe = ReplayPipeline(cfg, backend, scorer=scorer, proposer=detector,
                              use_relations=use_rel, name=arm)
        pipe.spatial_diversity = False            # replay the original tiles exactly
        run_experiment(pipeline=pipe, samples=samples, out_dir=str(out), run_name=arm,
                       resume=not args.check, cfg=cfg, dataset_info=info,
                       progress_every=int((cfg.get("run") or {}).get("progress_every", 10)))

    if args.check:
        recs = load_jsonl(out / "prop_det" / "predictions.jsonl")
        print("\n=== PREFLIGHT ===")
        for r in recs[-len(samples):]:
            sel = [s.get("chosen") for s in (r.get("artifacts") or {}).get("selection") or []]
            orig_sel = [s.get("chosen") for s in
                        (orig["b3_selected"][r["uid"]].get("artifacts") or {}).get("selection") or []]
            print(f"{r['uid']}: status={r['status']} objects={r.get('n_objects')} "
                  f"relations={r.get('n_relations')} tiles_match_original={sel == orig_sel} "
                  f"errors={len(r.get('errors') or [])}")
        print(f"Took {time.time() - t0:.0f}s for {len(samples)} items x 2 methods.")
        print("If objects > 0 and tiles_match_original=True, run the full experiment without --check.")
        print("(The 2 test items are kept and reused; the full run resumes from them.)")
        return

    analyze(out, args.orig_results)


if __name__ == "__main__":
    main()
