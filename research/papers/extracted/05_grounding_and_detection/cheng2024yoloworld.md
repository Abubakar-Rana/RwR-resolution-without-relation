# YOLO-World: Real-Time Open-Vocabulary Object Detection

- **Authors**: Tianheng Cheng, Lin Song, Yixiao Ge, Wenyu Liu, Xinggang Wang, Ying Shan
- **Year**: 2024
- **Venue**: CVPR 2024
- **arXiv**: 2401.17270
- **URL**: https://arxiv.org/abs/2401.17270
- **BibTeX Key**: `cheng2024yoloworld`

## Abstract
The YOLO series has established real-time object detection excellence in computer vision, but remains constrained by pre-defined fixed vocabularies. We introduce YOLO-World, a cutting-edge approach that enhances YOLO with real-time open-vocabulary detection capabilities through vision-language modeling. YOLO-World proposes a Re-parameterizable Vision-Language Path Aggregation Network (RepVL-PAN) and multi-modality contrastive pre-training. At inference time, offline text vocabulary embeddings are pre-computed and cached into convolutional weights, enabling real-time detection of arbitrary user concepts. YOLO-World delivers exceptional zero-shot performance and runs at up to 74 FPS on a single GPU.

## Key Extracted Contributions
1. Re-parameterizing text embeddings into convolutional weights enables real-time open-vocabulary detection.
2. Runs at 20-50 FPS (15-40ms per tile), compared to >2,000ms for a single VLM generation call.
3. High recall on small objects (cars, buildings, roads) in dense visual environments.
