#!/usr/bin/env python
"""Dataset preparation and inspection.

Loads XLRS-Bench through the adapter, materialises embedded images to the cache,
and writes a data report. Run this before the experiments so that:

  * image materialisation (the slow, one-off part) happens once, separately from
    the GPU runs, and a failure there is not mixed up with a model failure;
  * you can see the actual category labels and confirm they map onto the 16
    sub-tasks before any result depends on that mapping;
  * the evaluation subset is fixed and recorded, so every arm evaluates the same
    samples.

Outputs (under --out):
  data_report.json     counts by sub-task / L2 / family / relational group,
                       the resolved field map, and the raw column list
  samples.jsonl        the normalised sample list actually used (uids included),
                       which is the manifest the runs are expected to cover
  image_index.json     uid -> image path(s), used by the qualitative figures

    python scripts/01_prepare_data.py --config configs/main.yaml
    python scripts/01_prepare_data.py --config configs/dev.yaml --out data/dev
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ctsr.config import load_config, load_samples, relational_tasks  # noqa: E402
from ctsr.data.taxonomy import ALL_TASKS, canonical_task, relational_group  # noqa: E402
from ctsr.utils.io_utils import (JsonlWriter, atomic_write_json, ensure_dir,  # noqa: E402
                                 write_csv)
from ctsr.utils.logging_utils import get_logger  # noqa: E402
from ctsr.utils.seed import set_seed  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="Prepare and inspect the XLRS-Bench data")
    ap.add_argument("--config", default="configs/default.yaml")
    ap.add_argument("--set", dest="overrides", action="append", default=[],
                    metavar="key.path=value")
    ap.add_argument("--out", default="data/prepared")
    ap.add_argument("--probe-images", type=int, default=5,
                    help="open this many images to verify size and tile plan")
    args = ap.parse_args()

    out = ensure_dir(args.out)
    log = get_logger("prepare", logfile=out / "prepare.log")

    cfg = load_config(args.config, args.overrides)
    set_seed(int(cfg.get("seed", 1234)))

    log.info("Loading dataset: %s (%s)",
             (cfg.get("data") or {}).get("name_or_path"),
             (cfg.get("data") or {}).get("source"))
    samples, info = load_samples(cfg)

    if not samples:
        log.error("No samples were loaded. Check data.source / data.name_or_path, "
                  "and set data.field_map if the columns differ from the verified "
                  "lite schema (path, index, question, 'multi-choice options', "
                  "answer, category, 'l2-category', image).")
        return 1

    # -- taxonomy sanity ---------------------------------------------------
    rel_set = relational_tasks(cfg)
    by_task = Counter(s.task for s in samples)
    recognised = [t for t in by_task if t in ALL_TASKS]
    unrecognised = sorted(t for t in by_task if t not in ALL_TASKS)

    log.info("Recognised %d of the 16 XLRS-Bench sub-tasks in this split.",
             len(recognised))
    if unrecognised:
        log.warning(
            "These category labels do not map to a known sub-task and will be "
            "grouped as 'unknown' (excluded from BOTH the relational and "
            "non-relational arms): %s. Add aliases in ctsr/data/taxonomy.py if "
            "they are in fact known tasks.", unrecognised)
    missing = [t for t in ALL_TASKS if t not in by_task]
    if missing:
        log.info("Sub-tasks absent from this split: %s", missing)

    # -- write the sample manifest ----------------------------------------
    sample_path = out / "samples.jsonl"
    with JsonlWriter(sample_path, mode="w") as w:
        for s in sorted(samples, key=lambda x: x.uid):
            w.write(s.to_dict())
    log.info("Wrote %d samples to %s", len(samples), sample_path)

    image_index = {s.uid: s.image_paths for s in samples}
    atomic_write_json(out / "image_index.json", image_index)

    # -- probe a few images -----------------------------------------------
    probes = []
    if args.probe_images > 0:
        from ctsr.tiling.tiler import TiledImage
        tcfg = cfg.get("tiling") or {}
        step = max(1, len(samples) // max(1, args.probe_images))
        for s in sorted(samples, key=lambda x: x.uid)[::step][:args.probe_images]:
            try:
                with TiledImage(s.image_path,
                                tile_size=int(tcfg.get("tile_size", 1024)),
                                overlap=int(tcfg.get("overlap", 128)),
                                max_tiles=tcfg.get("max_tiles")) as ti:
                    d = ti.describe()
                    d["uid"] = s.uid
                    d["task"] = s.task
                    probes.append(d)
                    log.info("Probe %s: %dx%d (%.1f MP) -> %d tiles",
                             s.uid, ti.width, ti.height, ti.megapixels, len(ti.tiles))
            except Exception as exc:
                log.error("Probe failed for %s (%s): %s", s.uid, s.image_path, exc)
                probes.append({"uid": s.uid, "error": str(exc)[:300]})

    # -- report -----------------------------------------------------------
    rel_counts = Counter(relational_group(s.category, rel_set) for s in samples)
    report = dict(info)
    report.update({
        "config": args.config,
        "n_samples_used": len(samples),
        "relational_partition": {
            "tasks": sorted(rel_set),
            "counts": dict(rel_counts),
            "note": ("This partition is a design decision of the study, not part of "
                     "XLRS-Bench. Fix it before looking at results: the two "
                     "group-level tests are the confirmatory analysis."),
        },
        "recognised_subtasks": sorted(recognised),
        "unrecognised_categories": unrecognised,
        "absent_subtasks": missing,
        "image_probes": probes,
        "image_cache_dir": (cfg.get("data") or {}).get("cache_dir"),
    })
    atomic_write_json(out / "data_report.json", report)

    rows = [{"task": t, "l2": (ALL_TASKS.index(t) < 10 if t in ALL_TASKS else None),
             "group": relational_group(t, rel_set), "n": n}
            for t, n in by_task.most_common()]
    for r in rows:
        from ctsr.data.taxonomy import l2_group
        r["l2"] = l2_group(r["task"])
    write_csv(out / "data_counts.csv", rows)

    # -- console summary --------------------------------------------------
    print("\n" + "=" * 74)
    print("Prepared {} samples from {}".format(
        len(samples), (cfg.get("data") or {}).get("name_or_path")))
    print("=" * 74)
    print("Relational group:      {}".format(dict(rel_counts)))
    print("Task families:         {}".format(info.get("by_family")))
    print("Multi-image samples:   {}".format(info.get("n_multi_image")))
    print("Unscorable (no answer):{}".format(info.get("n_unscorable")))
    print("\nPer sub-task counts:")
    for t, n in by_task.most_common():
        mark = "R" if relational_group(t, rel_set) == "relational" else \
               ("N" if t in ALL_TASKS else "?")
        print("  [{}] {:<42} {}".format(mark, t, n))
    if unrecognised:
        print("\nWARNING: unrecognised categories -> {}".format(unrecognised))
    print("\nReport: {}".format(out / "data_report.json"))
    print("=" * 74)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
