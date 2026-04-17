import dotenv
dotenv.load_dotenv()

from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import MessagesState
from langgraph.graph.message import add_messages


class MessagesState(MessagesState):
    # Add any keys needed beyond messages, which is pre-built 
    pass

# Model
from langchain_openrouter import ChatOpenRouter
llm = ChatOpenRouter(model="openai/gpt-4o-mini")

def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

llm_with_tools = llm.bind_tools([multiply])
    
# Node
def tool_calling_llm(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

from langgraph.graph import StateGraph, START, END
# Build graph
builder = StateGraph(MessagesState)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_edge(START, "tool_calling_llm")
builder.add_edge("tool_calling_llm", END)
graph = builder.compile()

print(graph.get_graph().draw_mermaid())

messages = graph.invoke({"messages": HumanMessage(content="Multiply 2 and 3")})
for m in messages['messages']:
    m.pretty_print()
