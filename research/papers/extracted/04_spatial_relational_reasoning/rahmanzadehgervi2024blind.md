# Vision Language Models are Blind

- **Authors**: Pooya Rahmanzadehgervi, Logan Bolton, Mohammad Reza Taesiri, Anh Tuan Nguyen
- **Year**: 2024
- **Venue**: ACCV 2024
- **arXiv**: 2407.08581
- **URL**: https://arxiv.org/abs/2407.08581
- **BibTeX Key**: `rahmanzadehgervi2024blind`

## Abstract
Despite claims that Multimodal Large Language Models have achieved human-like visual understanding, we demonstrate that SOTA VLMs suffer from profound perceptual 'blindness' on simple geometric and spatial tasks. We construct the Blindness Benchmark, evaluating models on fundamental low-level visual tasks such as checking if two circles overlap, determining line intersections, counting simple geometric shapes, and tracing connectivity. Alarmingly, leading models—including GPT-4o, Claude-3.5-Sonnet, and open-source models—frequently fail on these tasks, performing close to random chance. We trace this blindness to the patch tokenization of Vision Transformers and the loss of dense pixel-level connectivity in visual projectors.

## Key Extracted Contributions
1. SOTA VLMs fail on elementary spatial tasks (e.g. line intersection, object adjacency) that a human child solves trivially.
2. Patch tokenization in ViTs destroys continuous line topology and boundary intersections.
3. Language model reasoning priors override visual evidence, causing confident confabulation on spatial configurations.
