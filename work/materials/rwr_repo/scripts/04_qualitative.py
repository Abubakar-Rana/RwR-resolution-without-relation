#!/usr/bin/env python
"""Qualitative figures and failure-case cards (plan section 10).

Selects the most informative samples - the proposed method's wins, its losses,
and cases both arms failed - and produces, for each:

  * a scene-graph overlay on the image, with cross-tile edges highlighted
  * an overview-versus-crops comparison
  * a markdown case card tracing every arm's answer, the objects and the relations

Losses are produced deliberately alongside wins. A qualitative section that shows
only successes is not evidence.

    python scripts/04_qualitative.py --results results/main \
        --image-index data/prepared/image_index.json --n 3
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ctsr.report.qualitative import (case_card, overlay_scene_graph,  # noqa: E402
                                     pick_interesting_cases, side_by_side)
from ctsr.utils.io_utils import (atomic_write_json, ensure_dir, load_jsonl,  # noqa: E402
                                 read_json)
from ctsr.utils.logging_utils import get_logger  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="Qualitative analysis figures")
    ap.add_argument("--results", required=True)
    ap.add_argument("--out", default=None, help="default: <results>/report/qualitative")
    ap.add_argument("--image-index", default=None,
                    help="uid -> image path JSON from 01_prepare_data.py")
    ap.add_argument("--baseline-arm", default="b3_selected")
    ap.add_argument("--proposed-arm", default="proposed_ctsr")
    ap.add_argument("--n", type=int, default=3, help="cases per category")
    ap.add_argument("--uids", nargs="+", default=None,
                    help="specific uids instead of automatic selection")
    ap.add_argument("--max-edges", type=int, default=60)
    args = ap.parse_args()

    out = ensure_dir(args.out or (Path(args.results) / "report" / "qualitative"))
    log = get_logger("qualitative", logfile=out / "qualitative.log")
    root = Path(args.results)

    # uid -> image path(s)
    image_lookup = {}
    if args.image_index:
        raw = read_json(args.image_index, default={}) or {}
        for uid, paths in raw.items():
            if isinstance(paths, list) and paths:
                image_lookup[uid] = paths[0]
            elif isinstance(paths, str):
                image_lookup[uid] = paths
        log.info("Loaded %d image paths from %s", len(image_lookup), args.image_index)
    else:
        log.warning("No --image-index given: overlays and crop comparisons will be "
                    "skipped (prediction records do not store image paths). "
                    "Case cards will still be written.")

    # all arms' predictions, indexed by uid
    by_arm = {}
    for arm_dir in sorted(p for p in root.iterdir() if p.is_dir()):
        pred = arm_dir / "predictions.jsonl"
        if pred.exists():
            by_arm[arm_dir.name] = {r["uid"]: r for r in load_jsonl(pred) if r.get("uid")}
    if not by_arm:
        log.error("No predictions found under %s", root)
        return 1
    log.info("Arms found: %s", sorted(by_arm))

    if args.uids:
        picks = {"selected": list(args.uids)}
    else:
        picks = pick_interesting_cases(
            args.results, baseline_arm=args.baseline_arm,
            proposed_arm=args.proposed_arm, n_each=args.n)
    log.info("Cases selected: %s", {k: len(v) for k, v in picks.items()})

    made = {"picks": picks, "cards": {}, "figures": {}}
    for kind, uids in picks.items():
        for uid in uids:
            per_arm = {arm: recs.get(uid) for arm, recs in by_arm.items()}
            if not any(per_arm.values()):
                log.warning("uid %s not found in any arm; skipping.", uid)
                continue
            try:
                card = case_card(per_arm, uid, out)
                made["cards"].setdefault(kind, []).append(card)
            except Exception as exc:
                log.error("Case card failed for %s: %s", uid, exc)

            prop = per_arm.get(args.proposed_arm)
            img = image_lookup.get(uid)
            if not (prop and img):
                continue
            if not Path(img).exists():
                log.warning("Image for %s not on disk: %s", uid, img)
                continue
            stem = "{}_{}".format(kind, str(uid)[:36])
            for label, fn in (("overlay", lambda: overlay_scene_graph(
                                  prop, img, out, stem="qual_graph_" + stem,
                                  max_edges=args.max_edges)),
                              ("crops", lambda: side_by_side(
                                  img, prop, out, stem="qual_sbs_" + stem))):
                try:
                    paths = fn()
                    if paths:
                        made["figures"].setdefault(label, []).extend(paths)
                        log.info("%s figure for %s: %s", label, uid, paths[0])
                except Exception as exc:
                    log.error("%s figure failed for %s: %s", label, uid, exc)

    atomic_write_json(out / "qualitative_index.json", made)

    print("\n" + "=" * 74)
    print("QUALITATIVE OUTPUT")
    print("=" * 74)
    for kind, uids in picks.items():
        print("  {:<12} {}".format(kind, uids or "(none)"))
    n_figs = sum(len(v) for v in made["figures"].values())
    n_cards = sum(len(v) for v in made["cards"].values())
    print("\n  {} case card(s), {} figure file(s)".format(n_cards, n_figs))
    if not image_lookup:
        print("\n  Overlays skipped: re-run with --image-index "
              "data/prepared/image_index.json")
    print("\n  Written to: {}".format(out.resolve()))
    print("=" * 74)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
