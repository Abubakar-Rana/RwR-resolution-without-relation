# Machine Extraction: YOLO-World: Real-Time Open-Vocabulary Object Detection

- **BibTeX Key**: `cheng2024yoloworld`
- **Authors**: Tianheng Cheng, Lin Song, Yixiao Ge, Wenyu Liu, Xinggang Wang, Ying Shan
- **Venue**: CVPR 2024 (2024)
- **arXiv**: [2401.17270](https://arxiv.org/abs/2401.17270)
- **Code**: https://github.com/AILab-CVC/YOLO-World
- **Category**: 05_grounding_and_detection
- **Relevance**: 5 / 5 (Critical Efficiency & Grounding Prior)

## Abstract
We present YOLO-World, an innovative approach that enhances YOLOs with open-vocabulary detection capabilities via vision-language modeling. YOLO-World pre-computes offline text embeddings and re-parameterizes vision-language cross-attention into standard convolutions, achieving remarkable real-time open-vocabulary detection speed.

## Key Empirical Findings
1. Runs at 52 FPS (19ms per image) on modern GPUs, over 10x faster than Grounding DINO.
2. Re-parameterizable RepVL-PAN eliminates text encoder runtime during visual inference.
3. Robust zero-shot transfer on aerial and small object categories (vehicles, storage tanks, aircraft).
4. Drop-in replacement for the 13.0s VLM object extraction step in the RwR pipeline.

## Authors' Stated Conclusions
Re-parameterized vision-language path aggregation enables true real-time open-vocabulary detection.

## Open Challenges & Future Scope
Oriented bounding box support for dense satellite ports.

## Architectural Profile
- **Vision**: YOLOv8 backbone with RepVL-PAN
- **Projector**: Text-guided cross-attention with re-parameterization
- **LLM**: CLIP Text Encoder (Offline embedded)
- **Tokens**: Dense anchor-free grid
