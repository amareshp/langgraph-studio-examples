# AGENTS.md

Guidance for AI coding agents working in this repository.

## Keeping docs current

- **Update this file** whenever the app's structure changes: new graphs, modules,
  directories, dependencies, environment variables or conventions.
- **Update `README.md` in the same change** so the user-facing setup, run instructions,
  agent table and project-structure tree stay accurate.

## Overview

Example LangGraph agents served locally by the LangGraph Agent Server (`langgraph dev`)
and visualized in LangSmith Studio.

## Tooling

- Package and environment management: **uv** (`pyproject.toml`, `uv.lock`, `.python-version`).
  - Add runtime deps: `uv add <pkg>`; dev-only deps: `uv add --dev <pkg>`.
  - Run anything through uv: `uv run ...`.
- Python 3.12.
- Dev server: `langgraph-cli[inmem]` (dev dependency). Start with `uv run langgraph dev`.

## Structure

| Path                | Purpose |
| ------------------- | ------- |
| `comedian_agent.py` | `comedian_agent` graph. State: `prompt` (input) → `joke` (output). One node, `write_joke`, calls an OpenAI chat model via `init_chat_model`. Exports the compiled graph as `graph`, compiled with `name="comedian-agent"` so LangSmith traces carry that name. |
| `langgraph.json`    | Agent Server config. Maps graph IDs to `module:variable` and loads `.env`. Register every new graph here. |
| `pyproject.toml`    | Project metadata and dependencies. |
| `.env`              | Local secrets and LangSmith settings. Git-ignored; never commit it. |

## Environment variables

| Variable | Purpose |
| -------- | ------- |
| `LANGSMITH_API_KEY` | Required for Studio and tracing. |
| `LANGSMITH_AGENT_ID` | LangSmith agent that traces are addressed to (`comedian-agent`). Must be lowercase letters, digits and hyphens only, so it differs from the graph ID `comedian_agent`. |
| `LANGSMITH_AGENT_ENVIRONMENT` | Environment of that agent (e.g. `production`). |
| `LANGSMITH_TRACING` | `true` sends traces to LangSmith; `false` keeps all data local. |
| `LANGSMITH_ENDPOINT` | LangSmith API endpoint (`https://api.smith.langchain.com`). |
| `OPENAI_API_KEY` | Required by the OpenAI model. |
| `OPENAI_MODEL` | Optional model override (default `openai:gpt-5.5`). |

Values in `.env` override variables already set in the environment: agents call
`load_dotenv(override=True)` at import time. Keep this behaviour in new agents.

## Conventions

- One graph per top-level `*_agent.py` module, exporting the compiled graph as `graph`.
- Pass `name=<LANGSMITH_AGENT_ID>` to `compile()` so the trace name matches the LangSmith
  agent; otherwise traces are named "LangGraph".
- Each agent module keeps a `__main__` block so it can be run with `uv run python <file> ...`.
- After adding a graph, register it in `langgraph.json` and check that it loads with
  `uv run python -c "from <module> import graph"`.
