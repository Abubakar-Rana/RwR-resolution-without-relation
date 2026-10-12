# Machine Extraction: Arbitrary-Oriented Object Detection in Remote Sensing: A Survey

- **BibTeX Key**: `yang2024orientedrssurvey`
- **Authors**: Xue Yang, Junchi Yan, Qi Ming, Wentao Wang, Xian Sun, Kun Fu
- **Venue**: IEEE TPAMI 2024 (2024)
- **arXiv**: [2112.00344](https://arxiv.org/abs/2112.00344)
- **Code**: https://github.com/open-mmlab/mmrotate
- **Category**: 05_grounding_and_detection
- **Relevance**: 4 / 5 (Comprehensive Domain Survey)

## Abstract
Detecting arbitrary-oriented objects in remote sensing imagery faces unique challenges including boundary discontinuities, extreme aspect ratios, and densely packed targets. We systematically categorize oriented detectors, loss formulations (KLD, GWD), and benchmarks.

## Key Empirical Findings
1. Gaussian Wasserstein Distance (GWD) and Kullback-Leibler Divergence (KLD) loss resolve angle periodicity issues.
2. Oriented detection is essential for port, airport, and urban remote sensing.
3. Standard horizontal bounding boxes reduce effective IoU by over 50% on rotated elongated targets.

## Authors' Stated Conclusions
Oriented detection requires specialized angle-invariant loss formulations to handle boundary discontinuity.

## Open Challenges & Future Scope
Open-vocabulary oriented detection with vision-language foundation models.

## Architectural Profile
- **Vision**: Surveys 50+ detectors (MMRotate)
- **Projector**: N/A
- **LLM**: None
- **Tokens**: N/A
