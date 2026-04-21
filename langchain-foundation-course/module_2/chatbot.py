import dotenv
import sqlite3

from typing import Literal
from langchain_core.messages import HumanMessage, SystemMessage, RemoveMessage
from langgraph.graph import MessagesState
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver

from langchain_openrouter import ChatOpenRouter

dotenv.load_dotenv()  # Load environment variables from .env file

model = ChatOpenRouter(model="openai/gpt-4o-mini", temperature=0)

USE_SQLITE_DB = True


# State class to store messages and summary
class State(MessagesState):
    summary: str


def call_model(state: State):
    summary = state.get("summary", "")

    # If there is summary, then we add it to messages
    if summary:
        print(f"Using summary: {summary}")
        system_message = f"Summary of conversation earlier: {summary}"
        messages = [SystemMessage(content=system_message)] + state["messages"]
    else:
        messages = state["messages"]

    response = model.invoke(messages)
    return {"messages": [response]}


def should_continue(state: State) -> Literal["summarize_conversation", "__end__"]:
    """Return the next node to execute."""
    messages = state["messages"]

    if len(messages) > 6:
        return "summarize_conversation"

    return END


def summarize_conversation(state: State):
    summary = state.get("summary", "")

    if summary:
        # If a summary already exists, add it to the prompt
        summary_message = (
            f"This is summary of the conversation to date: {summary}\n\n"
            "Extend the summary by taking into account the new messages above:"
        )
    else:
        summary_message = "Create a summary of the conversation above:"

    # Add prompt to our history
    messages = state["messages"] + [HumanMessage(content=summary_message)]
    response = model.invoke(messages)

    # Delete all but the 2 most recent messages and add our summary to the state
    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    return {"summary": response.content, "messages": delete_messages}


# Define a new graph
workflow = StateGraph(State)
workflow.add_node("conversation", call_model)
workflow.add_node("summarize_conversation", summarize_conversation)

# Set the entrypoint as conversation
workflow.add_edge(START, "conversation")
workflow.add_conditional_edges("conversation", should_continue)
workflow.add_edge("summarize_conversation", END)

# Compile
if not USE_SQLITE_DB:
    memory = MemorySaver()
    graph = workflow.compile(checkpointer=memory)
else:
    # It is important to set check_same_thread to False, as LangGraph may access the database from multiple threads.
    conn = sqlite3.connect("chatbot_memory.db", check_same_thread=False)
    memory = SqliteSaver(conn=conn)
    graph = workflow.compile(checkpointer=memory)


if __name__ == "__main__":
    config = {"configurable": {"thread_id": "chatbot-thread"}}

    while True:
        user_input = input("User: ").strip()

        if user_input.lower() in ["exit", "quit"]:
            break

        if not user_input:
            continue

        result = graph.invoke(
            {"messages": [HumanMessage(content=user_input)]},
            config=config,
        )
        assistant_message = result["messages"][-1]
        print(f"Assistant: {assistant_message.content}")
