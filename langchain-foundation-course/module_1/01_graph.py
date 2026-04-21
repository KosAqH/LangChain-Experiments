import dotenv
import random

from pathlib import Path
from typing import Literal
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END

BASE_DIR = Path(__file__).resolve().parent.parent
dotenv.load_dotenv(BASE_DIR / ".env")


## State is a dictionary that holds the state of the graph. Each node can read and write to this state.
class State(TypedDict):
    graph_state: str


## Node is a function that takes the state as input and returns a dictionary that will be merged into the state.
def node_1(state):
    print("---Node 1---")
    return {"graph_state": state["graph_state"] + " I am"}


def node_2(state):
    print("---Node 2---")
    return {"graph_state": state["graph_state"] + " happy!"}


def node_3(state):
    print("---Node 3---")
    return {"graph_state": state["graph_state"] + " sad!"}


def decide_mood(state) -> Literal["node_2", "node_3"]:

    # Often, we will use state to decide on the next node to visit
    # user_input = state["graph_state"]

    # Here, let's just do a 50 / 50 split between nodes 2, 3
    if random.random() < 0.5:
        # 50% of the time, we return Node 2
        return "node_2"

    # 50% of the time, we return Node 3
    return "node_3"


# Build graph
builder = StateGraph(State)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

# Logic
builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", decide_mood)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

# Add
graph = builder.compile()

if __name__ == "__main__":
    # View
    print(graph.get_graph().draw_mermaid())

    ## Compiled graph implements `runnable` interface, so we can invoke it with an initial state.
    for _ in range(5):
        print(graph.invoke({"graph_state": "Hi, this is Lance."}))
