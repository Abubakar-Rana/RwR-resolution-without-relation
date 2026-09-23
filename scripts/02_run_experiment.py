#!/usr/bin/env python
"""Run one or more experimental arms.

The model is loaded ONCE and shared by every arm in the invocation, which both
saves time and removes a confound: all arms in a single run see the same weights,
the same dtype and the same processor settings.

Arms are run in the order given. Each writes to `<out_dir>/<arm>/` and resumes
from whatever is already there, so an interrupted job is restarted with the same
command.

    # everything, in order
    python scripts/02_run_experiment.py --config configs/main.yaml

    # just the controlled comparison
    python scripts/02_run_experiment.py --config configs/main.yaml \
        --arms b3_selected proposed_ctsr

    # an ablation
    python scripts/02_run_experiment.py --config configs/experiments/a3_shuffled_relations.yaml

    # a quick GPU sanity pass over 4 samples per task
    python scripts/02_run_experiment.py --config configs/dev.yaml --limit 20
"""
from __future__ import annotations

import argparse
import sys
import time
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ctsr.config import build_backend, load_config, load_samples  # noqa: E402
from ctsr.models.detector import build_proposer  # noqa: E402
from ctsr.pipelines.runner import ALL_ARMS, build_pipeline, run_experiment  # noqa: E402
from ctsr.tiling.selection import build_scorer  # noqa: E402
from ctsr.utils.errors import free_gpu  # noqa: E402
from ctsr.utils.io_utils import atomic_write_json, ensure_dir  # noqa: E402
from ctsr.utils.logging_utils import get_logger  # noqa: E402
from ctsr.utils.seed import set_seed  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="Run CTSR experimental arms")
    ap.add_argument("--config", default="configs/default.yaml")
    ap.add_argument("--set", dest="overrides", action="append", default=[],
                    metavar="key.path=value",
                    help="dotted config override, e.g. selection.top_k=8")
    ap.add_argument("--arms", nargs="+", default=None,
                    help="arms to run (default: run.arms from the config). "
                         "Choices: {}".format(", ".join(ALL_ARMS)))
    ap.add_argument("--out-dir", default=None, help="override run.out_dir")
    ap.add_argument("--limit", type=int, default=None,
                    help="cap the number of samples per arm (smoke testing)")
    ap.add_argument("--no-resume", action="store_true",
                    help="start fresh; existing results are moved aside, not deleted")
    ap.add_argument("--keep-going", action="store_true",
                    help="continue to the next arm if one fails outright")
    args = ap.parse_args()

    cfg = load_config(args.config, args.overrides)
    run_cfg = cfg.get("run") or {}
    out_dir = args.out_dir or run_cfg.get("out_dir", "results")
    arms = args.arms or run_cfg.get("arms") or ALL_ARMS
    resume = (not args.no_resume) and bool(run_cfg.get("resume", True))

    out_root = ensure_dir(out_dir)
    log = get_logger("run", logfile=out_root / "run.log")
    set_seed(int(cfg.get("seed", 1234)))

    log.info("Config: %s", args.config)
    log.info("Arms:   %s", arms)
    log.info("Output: %s (resume=%s)", out_root.resolve(), resume)

    unknown = [a for a in arms if a not in ALL_ARMS]
    if unknown:
        log.error("Unknown arm(s) %s. Choices: %s", unknown, ALL_ARMS)
        return 2

    # -- data --------------------------------------------------------------
    log.info("Loading samples...")
    try:
        samples, dataset_info = load_samples(cfg)
    except Exception as exc:
        log.exception("Dataset loading failed")
        print("\nDataset loading failed: {}: {}".format(type(exc).__name__, exc))
        print("Run `python scripts/00_check_env.py --config {} --check-data` to "
              "diagnose.".format(args.config))
        return 1
    if not samples:
        log.error("No samples loaded; nothing to run.")
        return 1
    log.info("Loaded %d samples across %d sub-tasks.",
             len(samples), len(dataset_info.get("by_task") or {}))

    # -- model (loaded once, shared) --------------------------------------
    log.info("Initialising the VLM backend...")
    backend = build_backend(cfg)
    try:
        backend.load()
    except Exception as exc:
        log.exception("Backend failed to load")
        print("\nBackend failed to load: {}: {}".format(type(exc).__name__, exc))
        print("Run `python scripts/00_check_env.py --load-model` to diagnose. To "
              "validate the pipeline without a GPU, use --set model.backend=stub.")
        return 1
    if getattr(backend, "is_stub", False):
        log.warning("STUB BACKEND IN USE - results are placeholders, not findings.")

    # Selection and detection modules are shared across arms that use them, for
    # the same reason the model is: identical behaviour, no per-arm confound.
    scorer = None
    proposer = None
    if any(a in ("b3_selected", "proposed_ctsr") for a in arms):
        log.info("Building the tile scorer and the region proposer...")
        try:
            scorer = build_scorer(cfg.get("selection") or {}, backend)
        except Exception as exc:
            log.exception("Tile scorer construction failed")
            print("\nTile scorer failed: {}. Try --set selection.scorer=saliency "
                  "(no extra weights needed).".format(exc))
            return 1
        try:
            proposer = build_proposer(cfg.get("detection") or {}, backend)
        except Exception as exc:
            log.exception("Region proposer construction failed")
            print("\nRegion proposer failed: {}".format(exc))
            return 1

    # -- run each arm ------------------------------------------------------
    summaries = {}
    t_all = time.perf_counter()
    exit_code = 0

    for arm in arms:
        log.info("=" * 70)
        log.info("ARM: %s", arm)
        log.info("=" * 70)
        try:
            pipeline = build_pipeline(arm, cfg, backend, scorer=scorer, proposer=proposer)
            summaries[arm] = run_experiment(
                pipeline=pipeline,
                samples=samples,
                out_dir=out_root,
                run_name=arm,
                resume=resume,
                limit=args.limit,
                retry_errors=bool(run_cfg.get("retry_errors", True)),
                cfg=cfg,
                dataset_info=dataset_info,
                progress_every=int(run_cfg.get("progress_every", 10)),
            )
            log.info("Arm %s summary: %s", arm, summaries[arm])
        except KeyboardInterrupt:
            log.warning("Interrupted during arm %s. Completed results are on disk; "
                        "re-run the same command to resume.", arm)
            exit_code = 130
            break
        except Exception as exc:
            log.exception("Arm %s failed", arm)
            summaries[arm] = {"error": "{}: {}".format(type(exc).__name__, exc),
                              "traceback": traceback.format_exc()[-3000:]}
            exit_code = 1
            if not args.keep_going:
                log.error("Stopping. Pass --keep-going to continue with the next arm.")
                break
        finally:
            free_gpu()

    atomic_write_json(out_root / "run_summary.json", {
        "config": args.config,
        "arms": arms,
        "elapsed_minutes": round((time.perf_counter() - t_all) / 60.0, 2),
        "backend_is_stub": bool(getattr(backend, "is_stub", False)),
        "summaries": summaries,
    })

    print("\n" + "=" * 74)
    print("Run complete in {:.1f} min".format((time.perf_counter() - t_all) / 60.0))
    print("=" * 74)
    for arm, s in summaries.items():
        if "error" in s:
            print("  {:<16} FAILED: {}".format(arm, s["error"][:120]))
            continue
        acc = s.get("accuracy")
        print("  {:<16} n={:<5} acc={:<8} calls/sample={:<6} err={}".format(
            arm, s.get("n_records", 0),
            "{:.4f}".format(acc) if acc is not None else "--",
            "{:.2f}".format(s["mean_vlm_calls"]) if s.get("mean_vlm_calls") else "--",
            s.get("n_error", 0),
        ))
    if getattr(backend, "is_stub", False):
        print("\nNOTE: these numbers come from the STUB backend and are not results.")
    print("\nNext: python scripts/03_aggregate_results.py --results {}".format(out_root))
    print("=" * 74)

    try:
        backend.unload()
    except Exception:
        pass
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
