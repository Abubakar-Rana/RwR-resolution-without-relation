# Machine Extraction: Relational Inductive Biases, Deep Learning, and Graph Networks

- **BibTeX Key**: `battaglia2024relationalinductivebiases`
- **Authors**: Peter W. Battaglia, Jessica B. Hamrick, Victor Bapst, Alvaro Sanchez-Gonzalez, Vinicius Zambaldi, Mateusz Malinowski, Andrea Tacchetti, David Raposo, Adam Santoro, Ryan Faulkner, Caglar Gulcehre, Francis Song, Andrew Ballard, Justin Gilmer, George Dahl, Ashish Vaswani, Kelsey Allen, Charles Nash, Victoria Langston, Chris Dyer, Nicolas Heess, Daan Wierstra, Pushmeet Kohli, Matt Botvinick, Oriol Vinyals, Yujia Li, Razvan Pascanu
- **Venue**: arXiv preprint (2018)
- **arXiv**: [1806.01261](https://arxiv.org/abs/1806.01261)
- **Code**: https://github.com/deepmind/graph_nets
- **Category**: 08_scene_graphs_and_symbolic_geometry
- **Relevance**: 5 / 5 (Foundational Relational Theory)

## Abstract
We explore relational inductive biases in deep learning and introduce the Graph Network framework. We argue that combinatorial generalization is the core missing capability of standard deep neural networks and that structured graph representations provide the necessary inductive bias.

## Key Empirical Findings
1. Standard neural networks fail at combinatorial generalization because they lack explicit entity-relation factorization.
2. Graph Networks explicitly factorize computation into entities (nodes), relations (edges), and global context ($u$).
3. Relational inductive biases are mathematically required to solve spatial multi-hop reasoning.

## Authors' Stated Conclusions
Explicit relational inductive biases (entities and relations) are essential for human-like combinatorial generalization.

## Open Challenges & Future Scope
Unified neural-symbolic graph foundation models.

## Architectural Profile
- **Vision**: General Graph Network block
- **Projector**: Edge, Node, and Global update functions
- **LLM**: None
- **Tokens**: Entities and relations
