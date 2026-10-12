# Machine Extraction: Inner Monologue: Embodied Reasoning through Planning with Language Models

- **BibTeX Key**: `huang2024innermonologue`
- **Authors**: Wenlong Huang, Fei Xia, Ted Xiao, Harris Chan, Jacky Liang, Pete Florence, Andy Zeng, Jonathan Tompson, Igor Mordatch, Yevgen Chebotar, Pierre Sermanet, Noah Brown, Tomas Jackson, Linda Luu, Sergey Levine, Karol Hausman, Brian Ichter
- **Venue**: CoRL 2022 (2022)
- **arXiv**: [2207.05608](https://arxiv.org/abs/2207.05608)
- **Code**: https://innermonologue-robot.github.io
- **Category**: 09_embodied_and_3d_spatial_priors
- **Relevance**: 3 / 5 (Moderate Embodied Prior)

## Abstract
We investigate how environment feedback enables LLMs to perform embodied reasoning. By injecting perceptual feedback (success detection, scene description) back into the prompt history as an 'inner monologue', the model corrects mistakes and replans dynamically.

## Key Empirical Findings
1. Closed-loop perceptual feedback increases task completion rate from 32% to 78%.
2. Language models adapt plans when environmental obstacles are reported.
3. Prevents compounding execution errors.

## Authors' Stated Conclusions
Perceptual feedback loops are essential for robust long-horizon reasoning and error recovery.

## Open Challenges & Future Scope
Hierarchical multi-agent dialogue.

## Architectural Profile
- **Vision**: ViLD / CLIP Object Detectors
- **Projector**: Textual environment descriptions
- **LLM**: InstructGPT / PaLM
- **Tokens**: Multi-turn prompt history
