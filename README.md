# 🛰️ Ultra-High-Resolution Vision-Language Model Research

An evidence-based research lab and codebase focused on solving the **Resolution-without-Relation (RwR)** crossover dilemma in ultra-high-resolution multimodal AI.

---

## 🚪 The 3 Core Folders (Simple Navigation)

This entire repository is organized into exactly **three main directories**:

```
vlm/
├── 🛠️ work/        # All CODE, active experiments, and original paper materials
├── 📚 research/    # The KNOWLEDGE BASE, 240 paper reviews, and synthesis findings
└── 🗄️ archive/     # Historical AGENT profiles, prompts, and scratchpads
```

---

### 1. [`work/`](file:///d:/projects/research/vlm/work/) — Code, Experiments & Materials
*Everything runnable and the original paper documents live here.*
- **[Problem Statement Papers (`paper/`)](file:///d:/projects/research/vlm/work/paper/)**: The 3 foundational manuscripts (`main.pdf`, `CVC_2027_NL.pdf`, `CVC-27-Paper-NL.docx`).
- **[Completed Research Paper (`main.pdf`)](file:///d:/projects/research/vlm/work/paper/main.pdf)**: Ground-truth 13-page manuscript.
- **[Submission Word Draft (`CVC-27-Paper-NL.docx`)](file:///d:/projects/research/vlm/work/paper/CVC-27-Paper-NL.docx)**: Original paper manuscript.
- **[Cloned Baseline Repository (`rwr_repo/`)](file:///d:/projects/research/vlm/work/materials/rwr_repo/)**: Original GitHub codebase.
- **[Active Python Codebase (`src/`)](file:///d:/projects/research/vlm/work/src/)**: Clean modular models, data loaders, and evaluation scripts.
- **[Experiment Configurations (`experiments/`)](file:///d:/projects/research/vlm/work/experiments/)**: YAML runners for evaluation benchmarks.

### 2. [`research/`](file:///d:/projects/research/vlm/research/) — Knowledge Base, 240 Papers & Findings
*All reading materials, deep analyses, benchmarks, and Q&A guides live here.*
- **[Master Knowledge Base (`knowledge_base/`)](file:///d:/projects/research/vlm/research/knowledge_base/README.md)**: Master portal and executive guide.
- **[10-Paradigm Comparison Matrix](file:///d:/projects/research/vlm/research/knowledge_base/paradigms_and_solutions_matrix.md)**: Side-by-side analysis of all 10 VLM architectures.
- **[Failure Modes Troubleshooting Guide (Q&A)](file:///d:/projects/research/vlm/research/knowledge_base/failure_modes_and_solutions_qa.md)**: Diagnostic equations and fixes for the 7 primary VLM bugs.
- **[Interactive Q&A & Defense Guide (25 Questions)](file:///d:/projects/research/vlm/research/knowledge_base/interactive_qa_guide.md)**: Complete study & oral exam preparation guide.
- **[1-Page Track Dossiers (`one_page_dossiers/`)](file:///d:/projects/research/vlm/research/knowledge_base/one_page_dossiers/)**: 10 one-page summaries (Tracks 01 to 10).
- **[240 Structured Paper Reviews (`reviews/`)](file:///d:/projects/research/vlm/research/reviews/categories/)**: Granular critiques across 10 categories.
- **[Master Literature Catalog (`master_index.md`)](file:///d:/projects/research/vlm/research/reviews/indices/master_index.md)**: Searchable table of all 240 papers.
- **[Master Comparative Matrix](file:///d:/projects/research/vlm/research/findings/comparative_matrix.md)**: Ground-truth benchmark scores.
- **[Continuous Research Log](file:///d:/projects/research/vlm/research/findings/research_log.md)**: Chronological ledger of all milestones.

### 3. [`archive/`](file:///d:/projects/research/vlm/archive/) — Agents, Prompts & History
*Historical configurations and workspace scratchpads.*
- **[Agent Profiles & Prompts (`agents/`)](file:///d:/projects/research/vlm/archive/agents/)**: Operating guidelines and prompt templates.
- **[Superseded Experiments & Scratchpads](file:///d:/projects/research/vlm/archive/)**: Historical notes and debug logs.

---

## 🔬 The Core Problem in 30 Seconds

When evaluating Vision-Language Models on 8K satellite images (**XLRS-Bench-Lite**, 3,080 test items), zooming into local regions causes a counterintuitive trade-off:

$$\Delta_{\text{Perception}} = +4.1\text{ pp} \quad \text{vs.} \quad \Delta_{\text{Relation}} = -4.5\text{ pp}$$

| Method | Mechanism | Perception Acc | Relational Acc | Overall Acc | Per-Item Latency |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Direct Full Image** | Downscale to $448\text{px}$ overview | $42.6\%$ | **$44.5\%$** | **$43.1\%$** | **$3.0\text{s}$** |
| **Two-Stage Zoom** | Crop candidate boxes | **$46.7\%$** | $40.0\%$ | $42.4\%$ | $16.8\text{s}$ |
| **Oracle Router** | Optimal per-query switch | **$54.2\%$** | **$48.5\%$** | **$51.2\%$** | $8.0\text{s}$ |

- **Why zooming hurts relations**: Cropping severs global topological context (**Visual Myopia**).
- **Why text scene graphs fail**: Text triples act as semantic distractors ($-4.1\text{ pp}$ perception, $+0.0\text{ pp}$ relations).
- **The solution**: **Dual-Stream Anchored Routing** dispatches relational queries to direct overview ($3.0\text{s}$) and perception queries to dual-stream zoom ($4.2\text{s}$), capturing $+8.8\text{ pp}$ accuracy gains while cutting inference compute by $>70\%$.

---

## 📜 Agent Guidelines
All AI agents operating in this workspace must follow [`AGENTS.md`](file:///d:/projects/research/vlm/AGENTS.md).
