# Paper Reviews (`reviews/`)

This directory contains deep, 1-by-1 critical analyses of individual research papers.

---

## Directory Layout

- [`template.md`](file:///d:/projects/research/vlm/reviews/template.md): The mandatory review template. Every paper critique must adhere to this schema.
- `notes/`: Individual paper review documents, named using the convention `[YYYY]_[FirstAuthor]_[ShortTitle].md` (e.g., `2024_Liu_LLaVA_NeXT.md`).

---

## Review Standards for AI Agents

1. **Strictly Use the Template**: Copy [`template.md`](file:///d:/projects/research/vlm/reviews/template.md) when starting a new review.
2. **Relevance Justification**: Don't simply score relevance (1 to 5); explicitly dissect why the paper matters or does not matter to our problem statement in [`docs/problem_statement.md`](file:///d:/projects/research/vlm/docs/problem_statement.md).
3. **What It Adds vs. What It Doesn't**: Explicitly isolate the novel core from generic or reused components.
4. **Implementation Actionability**: Every review must answer: *"What specific module, loss term, dataset recipe, or hyperparameter should we try in our codebase?"*
