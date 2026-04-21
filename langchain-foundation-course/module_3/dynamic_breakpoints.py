from typing_extensions import TypedDict, NotRequired
from langgraph.graph import START, END, StateGraph
from langgraph.types import interrupt


class State(TypedDict):
    input: str
    approved: NotRequired[bool]


def step_1(state: State) -> State:
    print("---Step 1---")
    return state


def step_2(state: State) -> State:
    # Pause execution when the input is longer than 5 characters.
    if len(state["input"]) > 5 and not state.get("approved", False):
        interrupt(f"Received input that is longer than 5 characters: {state['input']}")

    print("---Step 2---")
    return state


def step_3(state: State) -> State:
    print("---Step 3---")
    return state


builder = StateGraph(State)
builder.add_node("step_1", step_1)
builder.add_node("step_2", step_2)
builder.add_node("step_3", step_3)
builder.add_edge(START, "step_1")
builder.add_edge("step_1", "step_2")
builder.add_edge("step_2", "step_3")
builder.add_edge("step_3", END)

graph = builder.compile()

if __name__ == "__main__":
    print("Running with short input:")
    graph.invoke({"input": "short"})

    # This will raise an interrupt at step_2
    print("\nRunning with long input:")
    long_input_state: State = {"input": "this is a long input", "approved": False}
    result = graph.invoke(long_input_state)

    if "__interrupt__" in result:
        print(f"Graph execution was interrupted: {result['__interrupt__'][0].value}")
        user_choice = input("Continue anyway? (yes/no): ").strip().lower()

        if user_choice in ["yes", "y"]:
            long_input_state["approved"] = True
            graph.invoke(long_input_state)
            print("Graph execution continued.")
        else:
            print("Graph execution stopped by user.")
