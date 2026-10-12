# Experiments & Benchmarking (`experiments/`)

This directory houses reproducible experiment run configurations, launch scripts, and tracking logs.

---

## Directory Contents

- `configs/`: YAML or JSON configuration files defining model backbones, training stages, hyperparameters, dataset mixtures, and evaluation suites.
- `runs/` *(gitignored)*: Local checkpoints, TensorBoard/WandB logs, and evaluation dumps.

---

## Guidelines for AI Agents

1. **Config-Driven Runs**: Never hardcode hyperparameter configurations inside python files. Always define an isolated config in `configs/` (e.g. `configs/2026-10-mlp-vs-resampler.yaml`).
2. **Log Run Artifacts**: Record run outcomes in [`findings/research_log.md`](file:///d:/projects/research/vlm/findings/research_log.md) when an experiment terminates.
