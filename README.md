# LangGraph Studio Examples

Example LangGraph agents that run locally on the LangGraph Agent Server and can be
visualized and debugged in [LangSmith Studio](https://docs.langchain.com/oss/python/langgraph/studio).

## Agents

| Graph ID         | File                | What it does                                      |
| ---------------- | ------------------- | ------------------------------------------------- |
| `comedian_agent` | `comedian_agent.py` | Takes a prompt and uses an OpenAI model to write a joke. |

## Prerequisites

- [uv](https://docs.astral.sh/uv/)
- Python 3.12+ (uv installs it automatically from `.python-version`)
- A [LangSmith](https://smith.langchain.com) API key
- An OpenAI API key (`OPENAI_API_KEY`)

## Setup

```bash
uv sync
```

Create a `.env` file in the project root (it is git-ignored):

```bash
LANGSMITH_API_KEY=lsv2...
LANGSMITH_AGENT_ID="comedian-agent"
LANGSMITH_AGENT_ENVIRONMENT="production"
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
```

`OPENAI_API_KEY` can live in `.env` or in your shell environment. Values in `.env`
**override** variables already set in the environment.

Optional variables:

- `OPENAI_MODEL` – model passed to `init_chat_model` (default `openai:gpt-5.5`)
- Set `LANGSMITH_TRACING=false` to keep all data local and send no traces to LangSmith

## Run

Run the agent once from the command line:

```bash
uv run python comedian_agent.py "cats who code"
```

Start the local Agent Server and open it in Studio:

```bash
uv run langgraph dev
```

- API: http://127.0.0.1:2024
- Studio: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024

In Studio, choose the `comedian_agent` graph and send an input such as
`{"prompt": "cats who code"}`. The result appears in the `joke` field of the state.

Traces appear in LangSmith in the `comedian-agent-production` tracing project
(`<LANGSMITH_AGENT_ID>-<LANGSMITH_AGENT_ENVIRONMENT>`), with each trace named `comedian-agent`.

Safari blocks `localhost` connections to Studio. Use `uv run langgraph dev --tunnel` instead.

## Project structure

```
.
├── comedian_agent.py   # Comedian graph (prompt -> joke)
├── langgraph.json      # Agent Server config: graphs + env file
├── pyproject.toml      # Project metadata and dependencies (uv)
├── uv.lock
├── .env                # Local secrets (not committed)
├── AGENTS.md           # Guide for AI coding agents working in this repo
└── README.md
```
