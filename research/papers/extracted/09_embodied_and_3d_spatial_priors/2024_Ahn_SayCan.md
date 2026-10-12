# Machine Extraction: Do As I Can, Not As I Say: Grounding Language in Robotic Affordances

- **BibTeX Key**: `ahn2024saycan`
- **Authors**: Michael Ahn, Anthony Brohan, Noah Brown, Yevgen Chebotar, Omar Cortes, Byron David, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Daniel Ho, Jasmine Hsu, Julian Ibarz, Brian Ichter, et al.
- **Venue**: CoRL 2022 (2022)
- **arXiv**: [2204.01691](https://arxiv.org/abs/2204.01691)
- **Code**: https://say-can.github.io
- **Category**: 09_embodied_and_3d_spatial_priors
- **Relevance**: 3 / 5 (Moderate Embodied Prior)

## Abstract
Language models understand what is semantically sensible, but not what is physically possible in a given state. SayCan factors decision-making into semantic probability (from an LLM) and affordance probability (from a learned value function), selecting actions that are both useful and feasible.

## Key Empirical Findings
1. Factoring decisions into semantic prior $\times$ visual affordance prevents physically impossible actions.
2. Achieves 84% execution success on long-horizon mobile manipulation.
3. Grounding language in physical feasibility is essential for real-world reliability.

## Authors' Stated Conclusions
Semantic plausibility must be multiplicatively gated by physical affordance and sensory feasibility.

## Open Challenges & Future Scope
Continuous affordance spaces.

## Architectural Profile
- **Vision**: Value Function CNN from visual state
- **Projector**: Product of probabilities $P_{LLM} \times P_{afford}$
- **LLM**: PaLM-540B
- **Tokens**: N/A
