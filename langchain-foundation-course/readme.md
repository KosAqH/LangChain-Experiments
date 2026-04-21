# LangGraph Foundation Course Experiments

This directory contains hands-on LangGraph examples from the LangGraph Foundation Course, organized by modules.

## What Is This

- `module_1/`: graph basics, chains, routers, and agent memory fundamentals
- `module_2/`: stateful chatbot with checkpointing
- `module_3/`: breakpoints and human-in-the-loop patterns
- `module_4/`: map-reduce and parallel research workflows
- `langgraph.json`: local graph mapping for LangGraph Studio/dev workflows

## Note

This code is based on the LangGraph Foundation Course examples, with small local modifications and fixes.

## How To Run

1. Install dependencies from the project root:

```bash
uv sync
```

2. Add API keys in `langchain-foundation-course/.env` (copy from `.env.example`).
3. Run any module example:

```bash
uv run .\langchain-foundation-course\module_1\01_graph.py
uv run .\langchain-foundation-course\module_2\chatbot.py
uv run .\langchain-foundation-course\module_4\research_experiment.py
```

4. Optional: run with LangGraph Studio/dev tooling from this directory (uses `langgraph.json`).
5. Optional: you can also debug traces using [LangSmith](https://eu.smith.langchain.com)

## Troubleshooting

### Chrome Local Network Access Error

Recent versions of Chrome (v142+) have stricter Private Network Access rules that may block access to LangSmith Studio.

Solution:

1. Click the lock/tune icon to the left of the URL in the address bar.
2. Find Local network access and set it to Allow.
3. Reload the LangSmith Studio page.
