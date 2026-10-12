# Reproduce every number, table and figure from the committed model outputs.
# No GPU required for the `analysis` chain; `runs` needs one (see README).

PY ?= python

.PHONY: all data analysis figures revision runs clean

all: analysis

data:            ## gunzip the committed per-item outputs
	$(PY) scripts/prepare_results.py

analysis: data   ## tables, figures, revision analyses and LaTeX macros
	$(PY) analysis/analyze.py --results results/main --out analysis
	$(PY) analysis/make_figures.py
	$(PY) analysis/run_all.py

figures: data    ## figures only
	$(PY) analysis/make_figures.py

revision: data   ## robustness, power, router, detector grounding
	$(PY) analysis/run_all.py

runs:            ## the four GPU arms, in order (35.6 GPU-h on one L40S)
	$(PY) scripts/00_check_env.py --load-model
	$(PY) scripts/01_prepare_data.py --config configs/main.yaml
	$(PY) scripts/02_run_experiment.py --config configs/main.yaml --arm b1_direct
	$(PY) scripts/02_run_experiment.py --config configs/main.yaml --arm b2_tiling
	$(PY) scripts/02_run_experiment.py --config configs/main.yaml --arm b3_selected
	$(PY) scripts/02_run_experiment.py --config configs/main.yaml --arm proposed_ctsr
	$(PY) scripts/03_aggregate_results.py --results results/main

clean:           ## remove the expanded per-item outputs
	$(PY) -c "import glob,os; [os.remove(f) for f in glob.glob(\"results/**/predictions.jsonl\", recursive=True)]"
