# Resolution Without Relations

Code, per-item model outputs and analysis for the paper **“Resolution Without Relations:
Quantifying the Perception–Reasoning Trade-off of Tile Selection in Ultra-High-Resolution Remote
Sensing.”**

Zooming into question-relevant tiles of an ultra-high-resolution (UHR) scene is the standard recipe
for UHR visual question answering. We measure what it costs. On XLRS-Bench-lite with
Qwen2.5-VL-7B-Instruct, selecting tiles **helps perception and hurts spatial relational reasoning**,
and handing the lost layout back to the model as an explicit relation graph **does not repair it** —
not even when an open-vocabulary detector fills in the objects the graph was missing.

## Findings

All numbers below are produced by the scripts in this repository from the committed per-item
outputs; the paper reads them from the same generated macro files.

| Method (identical VLM, greedy decoding) | VLM calls | MPix | Overall | Relational | Non-relational |
|---|---|---|---|---|---|
| Direct (whole image, downscaled) | 1.00 | 0.98 | 41.3 | 37.9 | 42.6 |
| Tiling (all tiles, no selection) | 9.15 | 7.83 | 37.8 | 34.0 | 39.0 |
| Selection (question-relevant tiles) | 6.10 | 7.53 | **43.1** | 33.4 | **46.7** |
| Proposed (selection + relation graph) | 6.10 | 7.53 | 42.7 | 33.4 | 46.2 |

*n* = 2,983 scored four-option questions (chance 25%), 800 relational / 2,123 non-relational.

1. **The crossover.** Direct → Selection is **+4.1 pp** on non-relational questions
   (*p* = 9×10⁻⁶) and **−4.5 pp** on relational ones (*p* = 0.004). The sign flip survives all
   **8** alternative definitions of the relational group (permutation *p* ≤ 0.031).
2. **The null.** Selection → Proposed is **+0.0 pp** relational (*p* = 1.00) under *matched* VLM
   calls and encoded pixels — the two arms are one class differing by a single boolean.
3. **Not an artefact of empty graphs.** With Grounding DINO supplying objects, empty scene graphs
   fall from 52% to 0% and cross-tile relations rise from 25% to 99%, yet the relational gain is
   only **+1.8 pp** (*p* = 0.18). The bottleneck is object **relevance**: ~10% of detected objects
   match a question keyword (most frequent label: `tree`, 15,350 instances).
4. **What does help.** A cross-validated router that decides *whether* to zoom reaches **44.3%**
   (**+1.2 pp** over always zooming, *p* = 0.0039) with **22% fewer** VLM calls; a label-free
   variant matches accuracy at 30% fewer calls. A per-question oracle over the two policies would
   reach 51.2%.

## Layout

```
ctsr/                 the pipeline package (tiling, selection, relations, prompts, VLM backend)
  data/               XLRS-Bench loading, task taxonomy, answer parsing
  spatial/            tile geometry, pairwise relations, scene-graph serialisation
  pipelines/          direct / tiling / hierarchical (Selection and Proposed share one class)
  prompts/            the exact prompt templates used in every arm
configs/              YAML configs; configs/main.yaml reproduces the reported run
scripts/              00..06, run in order; see “Reproduce” below
analysis/             analyse committed outputs -> tables, figures, LaTeX macros
notebooks/            single-notebook version of the pipeline
paper/                main.tex, refs.bib, figures/, generated analysis/*.tex
tools/                figure/asset helpers and the real example questions used in the paper
results/main/         the reported run: 4 arms x 3,080 per-item records (gzipped) + report tables
results/detector_grounding/  the detector-grounded experiment: 1,201 items x 2 arms
results/analysis_outputs/    everything the analysis scripts regenerate
```

`ctsr/pipelines/hierarchical.py` is where the compute match lives: `Selection` and `Proposed` are
the same class with `use_relations` false/true, so the relational comparison is paired and
call-for-call identical.

## Reproduce the analysis (no GPU, ~2 minutes)

Every per-item model output is committed, so all tables, figures and paper numbers rebuild offline.

```bash
pip install numpy scipy matplotlib pandas scikit-learn pyyaml
python scripts/prepare_results.py          # gunzip predictions.jsonl.gz in place
python analysis/analyze.py --results results/main --out analysis
python analysis/make_figures.py            # fig2..fig4, appendix figures
python analysis/run_all.py                 # robustness, power, router, detector analysis, paper assets
python analysis/sync_paper.py              # copy regenerated tables/macros/figures into paper/
```

`analysis/run_all.py` runs `r01`…`r07` in order and writes to `results/analysis_outputs/`:

| script | what it establishes |
|---|---|
| `r01_partition_robustness.py` | the crossover under 8 definitions of “relational” |
| `r02_null_power.py` | minimum detectable effect at 80% power (3.0 pp relational, 6.9 pp crossover) |
| `r03_router.py` | cross-validated router, 5 folds × 20 repeats, plus the label-free variant and the oracle |
| `r04_router_figure.py` | router accuracy/cost figure |
| `r05_detector_grounding.py` | detector-grounded arms, graph statistics, label-relevance analysis |
| `r06_grounding_figure.py` | grounding figure |
| `r07_paper_assets.py` | `paper/analysis/numbers_rev.tex` (93 macros), `table_partitions.tex`, `fig3` |

No number in the paper is typed by hand: `main.tex` reads `analysis/numbers.tex` and
`analysis/numbers_rev.tex`, both generated. Regenerating them and diffing against the committed
copies is the fastest way to check a claim.

## Reproduce the runs (GPU)

The reported run took **35.6 GPU-hours** on one NVIDIA L40S (44 GB), plus **4.2 GPU-hours** for the
detector-grounded experiment. Environment of record: Python 3.11.5, torch 2.13.0+cu130,
transformers 4.57.6, CUDA 13.0.

```bash
# 1. torch first, matched to your CUDA build (see requirements.txt), then:
pip install -r requirements.txt
python scripts/00_check_env.py --load-model      # verifies Qwen2.5-VL loads

# 2. data: XLRS-Bench-lite from HuggingFace (initiacms/XLRS-Bench-lite), cached under data/
python scripts/01_prepare_data.py --config configs/main.yaml

# 3. the four arms (resumable; re-running skips finished items)
python scripts/02_run_experiment.py --config configs/main.yaml --arm b1_direct
python scripts/02_run_experiment.py --config configs/main.yaml --arm b2_tiling
python scripts/02_run_experiment.py --config configs/main.yaml --arm b3_selected
python scripts/02_run_experiment.py --config configs/main.yaml --arm proposed_ctsr

# 4. tables and qualitative cases
python scripts/03_aggregate_results.py --results results/main
python scripts/04_qualitative.py --results results/main

# 5. the detector-grounded experiment (downloads Grounding DINO base)
python scripts/06_detector_grounding.py --results results/main --out results/detector_grounding
```

`configs/low_vram.yaml` runs the same protocol with 4-bit weights; `configs/smoke.yaml` uses the
stub backend and needs no GPU, which is the cheapest way to check the compute match (both
hierarchical arms report identical VLM calls and encoded pixels).

Exact decoding is greedy with a fixed seed, but generation on different GPUs, transformers versions
or attention kernels will not be bit-identical. Expect small per-item differences; the reported
effects are 4–6 pp with the CIs given above.

## Build the paper

`paper/` compiles with pdfLaTeX (Springer `llncs`, which ships with Overleaf):

```bash
cd paper && pdflatex main && bibtex main && pdflatex main && pdflatex main
```

## Data and licence

- **Code** in this repository: MIT (see `LICENSE`).
- **Benchmark.** Images and annotations are from
  [XLRS-Bench](https://arxiv.org/abs/2503.23771) (CVPR 2025) and are *not* redistributed here.
  Its annotations are released under CC BY-NC-SA; obtain them from the authors’ release and follow
  its terms. `results/` contains our model outputs (predicted option letters, token counts,
  timings, geometry and scene graphs) plus the question ids needed to join back to the benchmark.
- **Models.** Qwen2.5-VL-7B-Instruct and Grounding DINO base are downloaded from HuggingFace under
  their own licences; no weights are included here.
- 97 of the 3,080 loaded questions are excluded from scoring because the *Overall Land Use*
  category is multi-select rather than four-option; the exclusion is recorded in the coverage
  section of `results/main/report/aggregate.json`.

## Citation

```bibtex
@inproceedings{resolutionwithoutrelations,
  title     = {Resolution Without Relations: Quantifying the Perception--Reasoning
               Trade-off of Tile Selection in Ultra-High-Resolution Remote Sensing},
  author    = {TODO},
  booktitle = {Computer Vision Conference (CVC)},
  year      = {2027}
}
```
