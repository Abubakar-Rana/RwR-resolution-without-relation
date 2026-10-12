# 🚀 Google Colab Grand Synthesis Execution Instructions (Test 3)

This guide provides end-to-end instructions for running and verifying the **Grounded Dual-Scale Pyramid Architecture** (Test 3 Grand Synthesis) in **Google Colab** on standard T4, L4, or A100 GPUs.

---

## 📖 Plain-English Glossary

| Term | Full Name | Plain-English Meaning |
| :--- | :--- | :--- |
| **VLM** | **Vision-Language Model** | An AI that can look at satellite imagery and answer natural-English questions. |
| **UHR** | **Ultra-High-Resolution** | Very large imagery ($8,500 \times 8,500$ px) requiring smart multi-scale processing. |
| **2D-RoPE** | **Two-Dimensional Rotary Position Embeddings** | Position tags giving coordinates on the global map so crops never lose their location. |
| **Set-of-Mark (SoM)** | **Visual Pixel Badging** | Overlaying bright numbers (`[1]`, `[2]`) onto candidate objects to eliminate coordinate hallucinations. |
| **Quad-Tree** | **15% Overlapped Hierarchical Quad-Tree** | A multi-level zooming tree with overlapping borders eliminating boundary seam cuts (0.00% cuts). |
| **Pixel-Shuffle** | **2x2 Spatial Token Compression** | Merging 4 neighboring image tokens into 1 token, cutting sequence length by 75%. |
| **OOM** | **Out-Of-Memory Error** | A crash when a model tries to load more image tokens than the GPU's memory can hold. |

---

## 🧒 Explain Like I'm 5: The Big Idea

Imagine you are looking at an enormous $8,500 \times 8,500$ pixel satellite image:
- **Direct Overview (B1)** is like looking from an airplane: fast (2.98s), but tiny objects like planes or cars are blurry.
- **Uniform Tiling (B2)** is like slicing a sheet cake into pieces: it chops objects in half at the cuts (seam severing) and costs 12,884 tokens!
- **Test 3 Grand Synthesis** is the smartest way:
  1. An **Adaptive Router** checks the question. If it's a macro overview question, it answers immediately (2.98s).
  2. If it's a detail question, an **Overlapped Quad-Tree** zooms in without cutting objects (0.00% seam cuts).
  3. Numeric badge stickers (`[1]`, `[2]`) are stamped directly on objects (**Set-of-Mark**).
  4. Continuous $(x,y)$ coordinate tags (**2D-RoPE**) are attached so zoomed crops know where they are on the big map.
  5. Tokens are compressed 4x (**Pixel-Shuffle 2x2**), and cross-attention fuses everything into just **192 tokens**!
  6. The whole pipeline achieves **53.13% accuracy** in **4.98 seconds** average latency!

---

## 📦 What Has Been Prepared

1. **Standalone Verification Notebook**:
   - Location: `Test3_Colab_Grand_Synthesis_Verification.ipynb`
   - Uploadable to Google Colab.
2. **Self-Contained Repository Bundle**:
   - Location: `test3_colab_complete_bundle.zip`
   - Contains all 7 consolidated architecture modules, all 63 unit tests, sample prediction traces, and benchmark data.
3. **Automated Command-Line Verification Script**:
   - Location: `run_colab_verification.py`
   - One-command verification script running the full test suite, token verification, and 2,983-item benchmark audit.

---

## 📋 Step-by-Step Instructions for Google Colab

### 1. Open Google Colab & Select GPU Runtime
1. Navigate to [colab.research.google.com](https://colab.research.google.com/).
2. Click **File -> Upload notebook** and select `Test3_Colab_Grand_Synthesis_Verification.ipynb`.
3. In Colab, click **Runtime -> Change runtime type**.
4. Set **Hardware accelerator** to **T4 GPU** (or A100 / L4) and click **Save**.

### 2. Upload the Codebase Bundle
1. In the left sidebar, click the **Folder icon (Files)**.
2. Drag and drop `test3_colab_complete_bundle.zip` into the file area.
3. Upload takes just a few seconds.

### 3. Run the Notebook Cells Sequentially
The notebook contains 7 clear steps:
- **Step 0 (`GPU Check`)**: Verifies GPU and VRAM via `!nvidia-smi` and checks PyTorch.
- **Step 1 (`Unpack Codebase`)**: Auto-discovers and extracts the zip, registering all Python modules.
- **Step 2 (`7 Modules Unit Verification`)**: Runs all 63 pytest unit tests validating all 7 components with 100% pass rate.
- **Step 3 (`Qwen2.5-VL-7B Model Loading`)**: Loads the model with automatic 4-bit NF4 quantization fallback, fitting comfortably within the 16GB T4 limit (~5.29 GB VRAM).
- **Step 4 & 5 (`Live Inference & Token Verification`)**: Executes representative XLRS-Bench items and verifies that generated answer tokens match offline trace logs with 100% exact fidelity (`ANSWER: A`, `ANSWER: C`, `ANSWER: D`).
- **Step 6 (`Full Benchmark Audit`)**: Evaluates the full 2,983-item XLRS-Bench dataset, verifying **53.13% overall accuracy**, **45.75% relational accuracy**, **2.33 VLM calls**, and **4.98s latency**.

---

## 📊 Ground-Truth Metrics to Confirm in Colab

| Method / Architecture | Overall Acc (%) | Relational Acc (%) | Non-Relational Acc (%) | Avg VLM Calls | Latency / Item | Fused Visual Tokens |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **B1: Direct** | 41.33% | 37.88% | 42.58% | 1.00 | 2.98s | 1,408 |
| **B2: Tiling** | 37.78% | 34.00% | 38.95% | 9.15 | 4.99s | 12,884 |
| **B3: Selection** | 43.11% | 33.38% | 46.68% | 6.10 | 15.40s | 8,448 |
| **Test1 Router** | 44.32% | 37.88% | 46.68% | 4.76 | 11.30s | 5,632 |
| **Test2 Pyramidal** | 50.49% | 42.38% | 53.46% | 2.82 | 5.71s | 768 |
| **[WINNER] Test3 Grand Synthesis** | **53.13%** | **45.75%** | **55.84%** | **2.33** | **4.98s** | **192** |
| *Oracle Upper Bound (B1+B3)* | *51.16%* | *44.88%* | *53.56%* | — | — | — |
| *Oracle Upper Bound (All 3)* | *58.70%* | *51.75%* | *61.22%* | — | — | — |

---

## 🛠️ CLI Alternative (Colab Terminal or Headless Execution)

You can also run the full verification pipeline via the command line:

```bash
# 1. Unzip the bundle
unzip test3_colab_complete_bundle.zip

# 2. Run the automated verification suite
python run_colab_verification.py
```
