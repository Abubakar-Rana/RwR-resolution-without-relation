# Multi-Agent Coordination & Prompts (`agents/`)

This directory coordinates multiple AI assistants (OpenAI Codex, Anthropic Claude, Google Gemini/Antigravity, Cursor) collaborating across research and development tracks.

---

## Directory Layout

- [`prompts/`](file:///d:/projects/research/vlm/agents/prompts): Specialized system instructions and persona prompts for specific agent roles:
  - `literature_reviewer.md`: Prompt for critical paper dissection and deep reading.
  - `code_implementer.md`: Prompt for implementing model components from papers.
  - `synthesis_critic.md`: Prompt for challenging hypotheses and cross-paper gap analysis.
- [`workflows/`](file:///d:/projects/research/vlm/agents/workflows): Step-by-step procedures for agent handoffs and automated pipelines:
  - `literature_pipeline.md`: The 5-stage ingestion-to-review workflow.

---

## Instructions for AI Agents

1. When assuming a persona or executing a specialized task, load the corresponding prompt from `prompts/`.
2. Follow workflow stages outlined in `workflows/` without skipping verification steps.
