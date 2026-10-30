"""Comedian agent: a minimal LangGraph graph that turns a prompt into a joke."""

import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.graph import END, START, StateGraph

# Values in .env take precedence over variables already set in the environment.
load_dotenv(override=True)

MODEL = os.getenv("OPENAI_MODEL", "openai:gpt-5.5")
SYSTEM_PROMPT = (
    "You are a witty stand-up comedian. Write one short, original, "
    "family-friendly joke about whatever the user gives you. "
    "Reply with the joke only."
)


class State(TypedDict, total=False):
    prompt: str
    joke: str


model = init_chat_model(MODEL)


def write_joke(state: State) -> State:
    response = model.invoke(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": state["prompt"]},
        ]
    )
    return {"joke": response.text}


builder = StateGraph(State)
builder.add_node("write_joke", write_joke)
builder.add_edge(START, "write_joke")
builder.add_edge("write_joke", END)

# The name is used as the root run (trace) name in LangSmith.
graph = builder.compile(name="comedian-agent")


if __name__ == "__main__":
    import sys

    prompt = " ".join(sys.argv[1:]) or "programmers"
    print(graph.invoke({"prompt": prompt})["joke"])
