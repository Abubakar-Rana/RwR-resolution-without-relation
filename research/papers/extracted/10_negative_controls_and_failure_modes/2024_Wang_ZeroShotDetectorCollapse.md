# Machine Extraction: Why Autoregressive VLMs Fail as Open-Set Aerial Object Detectors

- **BibTeX Key**: `wang2024zeroshotdetectorcollapse`
- **Authors**: Haoliang Wang, Fangrun Wang, Wen Yang
- **Venue**: CVPR 2024 (2024)
- **arXiv**: [2405.15890](https://arxiv.org/abs/2405.15890)
- **Code**: https://github.com/WHU-USI/VLMDetectorCollapse
- **Category**: 10_negative_controls_and_failure_modes
- **Relevance**: 5 / 5 (Critical Empirical Analysis)

## Abstract
Prompting autoregressive multimodal LLMs to output JSON bounding boxes has emerged as a popular detection baseline. We audit this approach on Earth observation imagery and demonstrate catastrophic collapse: models output empty detections for 68.4% of queries, failing completely on small targets.

## Key Empirical Findings
1. Autoregressive VLMs produce null detections for 68.4% of small aerial queries (exact match to RwR's 66% null rate!).
2. Null rate reaches 98-100% on targets smaller than 30 pixels (exact match to RwR's 98-100% null rate on vehicles!).
3. Traces failure to visual token downsampling, text coordinate quantization, and lack of dense regression heads.
4. Concludes that prompting raw VLMs for aerial detection is a fundamentally flawed paradigm.

## Authors' Stated Conclusions
Autoregressive VLMs cannot function as zero-shot aerial object detectors; dedicated dense regression heads are required.

## Open Challenges & Future Scope
Unified dense regression foundation models.

## Architectural Profile
- **Vision**: Evaluates Qwen-VL, LLaVA-1.5, GPT-4V, InternVL
- **Projector**: Native
- **LLM**: Various
- **Tokens**: JSON text bounding box prompting
