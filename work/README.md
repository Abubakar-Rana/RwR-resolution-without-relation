# 🛠️ Work Directory: Codebase, Materials & Experiments

Welcome to the **Work** directory. This folder houses all runnable software, the original project papers, benchmark configurations, and tool scripts.

---

## 📂 Folder Structure

```
work/
├── paper/             # Core problem statement papers (main.pdf, CVC_2027_NL.pdf, CVC-27-Paper-NL.docx)
├── materials/         # Cloned external repository & references (rwr_repo/)
│   └── rwr_repo/      # Cloned source repository (RwR-resolution-without-relation)
│
├── src/               # Core modular Python codebase
│   ├── models/        # Vision encoders, multimodal connectors & LLM decoders
│   ├── evaluation/    # Metric calculators, McNemar test & evaluation loops
│   ├── data/          # XLRS-Bench loaders & patch slicing utilities
│   └── utils/         # Coordinate transforms & geometry math
│
├── experiments/       # Benchmarking pipelines & YAML configurations
│   └── configs/       # Experiment hyperparameters (Direct, Selection, Oracle)
│
└── skills/            # Research automation & synthesis toolchain
    └── literature_synthesizer/ # 240-paper corpus generator & knowledge base builder
```

---

## 🚀 Quick Reference

| Item | Path | Description |
| :--- | :--- | :--- |
| **Core Papers & Problem Statement** | [`paper/`](file:///d:/projects/research/vlm/work/paper/) | The 3 foundational manuscripts (`main.pdf`, `CVC_2027_NL.pdf`, `CVC-27-Paper-NL.docx`) |
| **Initial Paper PDF** | [`paper/main.pdf`](file:///d:/projects/research/vlm/work/paper/main.pdf) | The original 13-page research paper detailing the crossover effect |
| **Submission Word Doc** | [`paper/CVC-27-Paper-NL.docx`](file:///d:/projects/research/vlm/work/paper/CVC-27-Paper-NL.docx) | Full editable manuscript of the study |
| **Cloned Repo** | [`materials/rwr_repo/`](file:///d:/projects/research/vlm/work/materials/rwr_repo/) | The baseline GitHub implementation |
| **Active Source Code** | [`src/`](file:///d:/projects/research/vlm/work/src/) | Clean, modular PyTorch implementation |
| **Experiment Configs** | [`experiments/configs/`](file:///d:/projects/research/vlm/work/experiments/configs/) | YAML test runners |
