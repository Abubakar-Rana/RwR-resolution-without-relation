# Mind's Eye: Grounded Spatial Reasoning Through Simulation and Scene Graphs

- **Authors**: Ruibo Liu, Jason Wei, Shixiang Shane Gu, Te-Yen Wu, Soroush Vosoughi, Claire Cui, Denny Zhou, Andrew M. Dai
- **Year**: 2023
- **Venue**: ICLR 2023
- **arXiv**: 2210.05349
- **URL**: https://arxiv.org/abs/2210.05349
- **BibTeX Key**: `liu2023mindseye`

## Abstract
Large Language Models struggle with spatial, physical, and geometric reasoning when forced to rely solely on text representations. We propose Mind's Eye, a framework that grounds spatial reasoning by coupling language models with external physical simulation engines. When faced with a complex spatial query, the language model generates simulation code, executes it in a lightweight physics simulator, and observes the simulated spatial states to produce the final grounded answer. On challenging spatial benchmarks, Mind's Eye improves reasoning accuracy from 32.4% to over 85%, demonstrating the power of externalized simulation.

## Key Extracted Contributions
1. Language models generate spatial simulation code much more reliably than they generate direct spatial answers.
2. Externalizing spatial calculations (distance, collision, trajectory) eliminates geometric hallucination entirely.
3. Neuro-symbolic coupling allows the LLM to focus on semantic interpretation while delegating geometry to code.
