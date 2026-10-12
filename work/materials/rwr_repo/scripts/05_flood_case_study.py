#!/usr/bin/env python
"""Flood impact demonstration (plan section 11).

This is the qualitative application case: can the cross-tile representation
connect infrastructure objects to a hazard region when the two lie in different
parts of one ultra-high-resolution scene?

IMPORTANT, and stated plainly because it affects what may be claimed:

  * XLRS-Bench is not a flood dataset. This script therefore runs on imagery and
    questions that YOU supply, via a small manifest file. It does not pretend a
    flood benchmark exists inside XLRS-Bench.
  * Unless your manifest provides an `expected` field, there is no ground truth,
    so no accuracy is computed and none is reported. The output is a traceable
    answer plus the evidence it cites - which is the point of the demonstration,
    and is what the plan describes ("a qualitative application case").
  * Each question is answered twice, with and without the relation block, so the
    demonstration shows the same contrast as the main experiment rather than only
    the proposed method's output.

Manifest format (JSON):

    [
      {
        "id": "sindh_2022_tile_a",
        "image": "data/flood/scene_a.tif",
        "questions": [
          "Which schools are located inside the flooded area?",
          "How many health facilities are within the inundated region?"
        ],
        "expected": "optional free-text note used only for your own reading"
      }
    ]

If "questions" is omitted, the templates in ctsr/prompts/templates.py are used
with the facilities given by --facilities.

    python scripts/05_flood_case_study.py --config configs/main.yaml \
        --manifest data/flood/manifest.json --out results/flood
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ctsr.config import build_backend, load_config  # noqa: E402
from ctsr.data.schema import Sample  # noqa: E402
from ctsr.models.detector import build_proposer  # noqa: E402
from ctsr.prompts.templates import FLOOD_QUESTION_TEMPLATES, flood_case_prompt  # noqa: E402
from ctsr.spatial.dedup import cap_objects, merge_detections  # noqa: E402
from ctsr.spatial.relations import RelationConfig, build_relations  # noqa: E402
from ctsr.spatial.scene_graph import SceneGraph  # noqa: E402
from ctsr.tiling.selection import build_scorer, question_keywords, select_tiles  # noqa: E402
from ctsr.tiling.tiler import TiledImage  # noqa: E402
from ctsr.utils.compute import ComputeMeter  # noqa: E402
from ctsr.utils.errors import ErrorCollector, free_gpu, stage  # noqa: E402
from ctsr.utils.io_utils import (JsonlWriter, atomic_write_json, ensure_dir,  # noqa: E402
                                 read_json)
from ctsr.utils.logging_utils import get_logger  # noqa: E402
from ctsr.utils.seed import set_seed  # noqa: E402

DEFAULT_FACILITIES = ["schools", "health facilities", "bridges", "shelters"]


def build_questions(entry, facilities):
    qs = entry.get("questions")
    if qs:
        return [str(q) for q in qs if str(q).strip()]
    out = []
    for facility in facilities:
        for tpl in FLOOD_QUESTION_TEMPLATES:
            out.append(tpl.format(facility=facility))
    return out


def analyse_scene(image_path, question, cfg, backend, scorer, proposer, log):
    """Run the hierarchical pipeline once and return the graph plus both answers."""
    meter = ComputeMeter()
    collector = ErrorCollector()

    tcfg = cfg.get("tiling") or {}
    scfg = cfg.get("selection") or {}
    dcfg = cfg.get("detection") or {}
    mcfg = cfg.get("dedup") or {}
    rcfg = cfg.get("relations") or {}
    fcfg = cfg.get("final_call") or {}

    keywords = question_keywords(question)
    # Flood analysis needs the hazard region as well as the assets, so the water
    # terms are always in scope even when the question names only facilities.
    for extra in ("water", "flood", "flooded", "inundation", "river", "road"):
        if extra not in keywords:
            keywords.append(extra)

    with TiledImage(image_path,
                    tile_size=int(tcfg.get("tile_size", 1024)),
                    overlap=int(tcfg.get("overlap", 128)),
                    max_tiles=tcfg.get("max_tiles")) as ti:
        overview = ti.overview(int(tcfg.get("overview_side", 1024)))

        with stage("selection", collector) as sb:
            sb["value"] = scorer.score(ti, ti.tiles, question, None, meter=meter)
        scores = sb["value"]
        if scores:
            chosen = select_tiles(scores, ti.tiles, top_k=int(scfg.get("top_k", 5)),
                                  spatial_diversity=bool(scfg.get("spatial_diversity", True)),
                                  diversity_radius_frac=float(scfg.get("diversity_radius_frac", 0.04)),
                                  image_size=(ti.width, ti.height))
        else:
            log.warning("Tile scoring failed; using an even grid.")
            step = max(1, len(ti.tiles) // max(1, int(scfg.get("top_k", 5))))
            chosen = ti.tiles[::step][:int(scfg.get("top_k", 5))]

        with stage("extraction", collector) as eb:
            eb["value"] = proposer.extract(ti, chosen, question, keywords=keywords,
                                          meter=meter, collector=collector)
        extraction = eb["value"]
        objects = list(extraction.objects) if extraction else []

        if objects and bool(mcfg.get("enabled", True)):
            objects, _ = merge_detections(
                objects, image_size=(ti.width, ti.height),
                iou_thresh=float(mcfg.get("iou_thresh", 0.45)),
                cross_tile_iou_thresh=float(mcfg.get("cross_tile_iou_thresh", 0.25)),
                containment_thresh=float(mcfg.get("containment_thresh", 0.80)),
                seam_gap_px=float(mcfg.get("seam_gap_px", 8.0)),
                box_mode=str(mcfg.get("box_mode", "union")),
            )
        objects = cap_objects(objects, int(dcfg.get("max_objects_total", 60)),
                              keep_labels=keywords)

        relation_cfg = RelationConfig(
            max_neighbours=int(rcfg.get("max_neighbours", 6)),
            adjacency_gap_frac=float(rcfg.get("adjacency_gap_frac", 0.012)),
            near_dist_frac=float(rcfg.get("near_dist_frac", 0.06)),
            containment_thresh=float(rcfg.get("containment_thresh", 0.85)),
            use_compass=bool(rcfg.get("use_compass", True)),
            gsd_m_per_px=rcfg.get("gsd_m_per_px"),
            max_relations=int(rcfg.get("max_relations", 220)),
        )
        relations = build_relations(objects, (ti.width, ti.height), relation_cfg) \
            if objects else []
        graph = SceneGraph(objects=objects, relations=relations,
                           image_size=(ti.width, ti.height))

        crops = []
        for tile in chosen[:int(fcfg.get("attach_crops", 3))]:
            try:
                c = ti.crop(tile)
                side = int(fcfg.get("crop_thumb_side", 768))
                if max(c.size) > side:
                    c = c.copy()
                    c.thumbnail((side, side))
                crops.append(c)
            except Exception as exc:
                collector.add("attach_crop", exc)

        images = ([overview] if bool(fcfg.get("attach_overview", True)) else []) + crops

        from ctsr.prompts.templates import object_block_text
        obj_block = object_block_text(
            graph.object_lines(),
            "DETECTED OBJECTS (global coordinates, 0-1000 grid over the whole image):")
        rel_block = object_block_text(
            graph.relation_lines(include_metric=True) or ["(no relations established)"],
            "SPATIAL RELATIONS (computed geometrically from the global coordinates):")

        answers = {}
        for arm, block in (("without_relations", None), ("with_relations", rel_block)):
            prompt = flood_case_prompt(question, obj_block, block,
                                       n_regions=len(chosen))
            try:
                resp = backend.generate(prompt, images=images, max_new_tokens=400)
                meter.record_call(resp.prompt_tokens, resp.completion_tokens,
                                  resp.n_images, resp.pixels)
                answers[arm] = resp.text
            except Exception as exc:
                meter.record_call(failed=True)
                collector.add("answer:" + arm, exc)
                log.error("Answer generation failed for %s: %s", arm, exc)
                answers[arm] = ""

        for c in crops:
            try:
                c.close()
            except Exception:
                pass

        return {
            "image": str(image_path),
            "image_size": [ti.width, ti.height],
            "question": question,
            "keywords": keywords,
            "n_tiles_total": len(ti.tiles),
            "selected_tiles": [t.tile_id for t in chosen],
            "selected_boxes": [list(t.box) for t in chosen],
            "graph": graph.to_dict(),
            "graph_stats": graph.stats(),
            "answers": answers,
            "compute": meter.to_dict(),
            "errors": collector.to_list(),
        }


def main() -> int:
    ap = argparse.ArgumentParser(description="Flood impact qualitative demonstration")
    ap.add_argument("--config", default="configs/default.yaml")
    ap.add_argument("--set", dest="overrides", action="append", default=[])
    ap.add_argument("--manifest", required=True,
                    help="JSON list of {id, image, questions?, expected?}")
    ap.add_argument("--out", default="results/flood")
    ap.add_argument("--facilities", nargs="+", default=DEFAULT_FACILITIES,
                    help="used only when a manifest entry omits 'questions'")
    ap.add_argument("--max-questions", type=int, default=6,
                    help="cap per scene, since each question costs a full pipeline pass")
    ap.add_argument("--overlay", action="store_true",
                    help="also write a scene-graph overlay figure per scene")
    args = ap.parse_args()

    out = ensure_dir(args.out)
    log = get_logger("flood", logfile=out / "flood.log")

    cfg = load_config(args.config, args.overrides)
    set_seed(int(cfg.get("seed", 1234)))

    entries = read_json(args.manifest, default=None)
    if entries is None:
        log.error("Could not read the manifest: %s", args.manifest)
        return 1
    if isinstance(entries, dict):
        entries = entries.get("scenes") or entries.get("data") or [entries]
    if not isinstance(entries, list) or not entries:
        log.error("Manifest must be a non-empty JSON list of scene entries.")
        return 1

    missing = [e.get("image") for e in entries
               if not e.get("image") or not Path(str(e["image"])).exists()]
    if missing:
        log.error("These manifest images do not exist: %s", missing)
        return 1

    log.info("Initialising the model...")
    backend = build_backend(cfg)
    try:
        backend.load()
    except Exception as exc:
        log.exception("Backend failed to load")
        print("Backend failed to load: {}".format(exc))
        return 1
    if getattr(backend, "is_stub", False):
        log.warning("STUB BACKEND - the demonstration output is placeholder text.")

    scorer = build_scorer(cfg.get("selection") or {}, backend)
    proposer = build_proposer(cfg.get("detection") or {}, backend)

    results_path = out / "flood_results.jsonl"
    writer = JsonlWriter(results_path, mode="a")
    records = []
    t0 = time.perf_counter()

    try:
        for entry in entries:
            scene_id = str(entry.get("id") or Path(str(entry["image"])).stem)
            questions = build_questions(entry, args.facilities)[:args.max_questions]
            log.info("Scene %s: %d question(s)", scene_id, len(questions))

            for qi, question in enumerate(questions):
                log.info("  Q%d: %s", qi + 1, question)
                try:
                    rec = analyse_scene(entry["image"], question, cfg, backend,
                                        scorer, proposer, log)
                except KeyboardInterrupt:
                    raise
                except Exception as exc:
                    log.exception("Scene %s Q%d failed", scene_id, qi + 1)
                    rec = {"image": entry["image"], "question": question,
                           "error": "{}: {}".format(type(exc).__name__, exc)}
                rec["scene_id"] = scene_id
                rec["question_index"] = qi
                rec["expected_note"] = entry.get("expected")
                rec["backend_is_stub"] = bool(getattr(backend, "is_stub", False))
                writer.write(rec)
                records.append(rec)

                if args.overlay and "graph" in rec:
                    try:
                        from ctsr.report.qualitative import overlay_scene_graph
                        pseudo = {
                            "uid": "{}_q{}".format(scene_id, qi),
                            "task": "Flood impact (qualitative)",
                            "n_tiles_total": rec.get("n_tiles_total"),
                            "artifacts": {
                                "scene_graph": rec["graph"],
                                "selection": [{"chosen": rec.get("selected_tiles", [])}],
                                "tile_size": (cfg.get("tiling") or {}).get("tile_size", 1024),
                                "overlap": (cfg.get("tiling") or {}).get("overlap", 128),
                            },
                        }
                        paths = overlay_scene_graph(pseudo, entry["image"], out)
                        if paths:
                            log.info("  overlay: %s", paths[0])
                    except Exception as exc:
                        log.error("Overlay failed: %s", exc)
    except KeyboardInterrupt:
        log.warning("Interrupted; %d record(s) written.", len(records))
    finally:
        writer.close()
        free_gpu()

    # -- markdown write-up -------------------------------------------------
    md = ["# Flood impact demonstration", "",
          "Qualitative case study (research plan section 11). Each question was "
          "answered twice from the same evidence: once WITHOUT the cross-tile "
          "relation block and once WITH it.", ""]
    if any(r.get("backend_is_stub") for r in records):
        md += ["> **Stub backend was used. The text below is placeholder output, "
               "not a result.**", ""]
    md += ["No accuracy is reported: these scenes have no ground-truth annotation. "
           "The claim being illustrated is that the answer cites specific detected "
           "objects and that the relation block supplies the object-to-hazard links "
           "spanning different parts of the scene.", ""]

    for rec in records:
        md.append("## {} - {}".format(rec.get("scene_id"), rec.get("question")))
        if rec.get("error"):
            md += ["", "FAILED: `{}`".format(rec["error"]), ""]
            continue
        gs = rec.get("graph_stats") or {}
        md += [
            "",
            "- Image: `{}` ({} x {})".format(rec.get("image"),
                                             *(rec.get("image_size") or [0, 0])),
            "- Tiles: {} total, {} selected ({})".format(
                rec.get("n_tiles_total"), len(rec.get("selected_tiles") or []),
                rec.get("selected_tiles")),
            "- Objects: {} | relations: {} | cross-tile: {} ({})".format(
                gs.get("n_objects"), gs.get("n_relations"), gs.get("n_cross_tile"),
                gs.get("cross_tile_fraction")),
            "- VLM calls: {}".format((rec.get("compute") or {}).get("n_vlm_calls")),
            "",
            "**Without relations**", "", "> " +
            str((rec.get("answers") or {}).get("without_relations", "")).replace("\n", "\n> "),
            "",
            "**With cross-tile relations**", "", "> " +
            str((rec.get("answers") or {}).get("with_relations", "")).replace("\n", "\n> "),
            "",
        ]
        if rec.get("expected_note"):
            md += ["*Analyst note:* {}".format(rec["expected_note"]), ""]

    (out / "flood_report.md").write_text("\n".join(md), encoding="utf-8")
    atomic_write_json(out / "flood_summary.json", {
        "n_scenes": len({r.get("scene_id") for r in records}),
        "n_questions": len(records),
        "n_failed": sum(1 for r in records if r.get("error")),
        "elapsed_minutes": round((time.perf_counter() - t0) / 60.0, 2),
        "backend_is_stub": any(r.get("backend_is_stub") for r in records),
        "mean_cross_tile_relations": (
            sum((r.get("graph_stats") or {}).get("n_cross_tile", 0) for r in records)
            / len(records)) if records else None,
    })

    print("\n" + "=" * 74)
    print("FLOOD CASE STUDY")
    print("=" * 74)
    print("  scenes:     {}".format(len({r.get("scene_id") for r in records})))
    print("  questions:  {}".format(len(records)))
    print("  failed:     {}".format(sum(1 for r in records if r.get("error"))))
    print("\n  report:  {}".format(out / "flood_report.md"))
    print("  records: {}".format(results_path))
    print("=" * 74)

    try:
        backend.unload()
    except Exception:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
