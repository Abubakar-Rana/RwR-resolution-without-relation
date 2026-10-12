# Segment Anything

- **Authors**: Alexander Kirillov, Eric Mintun, Nikhila Ravi, Hanzi Mao, Chloe Rolland, Laura Gustafson, Tete Xiao, Spencer Whitehead, Alexander C. Berg, Wan-Yen Lo, Piotr Dollár, Ross Girshick
- **Year**: 2023
- **Venue**: ICCV 2023
- **arXiv**: 2304.02643
- **URL**: https://arxiv.org/abs/2304.02643
- **BibTeX Key**: `kirillov2023sam`

## Abstract
We present the Segment Anything project: a new task, model, and dataset for image segmentation. We build the largest segmentation dataset to date (over 1 billion masks on 11 million images) and design the promptable Segment Anything Model (SAM). SAM executes real-time promptable segmentation conditioned on foreground points, bounding boxes, or rough text prompts. SAM exhibits remarkable zero-shot generalization across diverse image distributions, including medical, aerial, and microscopy imagery.

## Key Extracted Contributions
1. Promptable zero-shot segmentation generalizes robustly to satellite and aerial imagery without fine-tuning.
2. Converting bounding boxes into precise pixel segmentation masks eliminates background noise and resolves exact shape boundaries.
3. High-capacity ViT image encoder can be evaluated once, with sub-10ms mask decoding.
