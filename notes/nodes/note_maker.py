from langchain_openrouter import ChatOpenRouter
from prompts import NOTE_SYSTEM_PROMPT
from models import NoteState


def note_maker_node(state: NoteState) -> dict:
    """Generates a note from the page content using the configured LLM."""
    llm = ChatOpenRouter(model="google/gemini-2.5-flash")

    system_prompt = NOTE_SYSTEM_PROMPT.format(
        topic=state["topic"],
        hints=state["hints"],
        references="\n".join(state["source_urls"]),
    )

    messages = [
        ("system", system_prompt),
        ("human", state["page_content"]),
    ]

    response = llm.invoke(messages)

    return {"note": response.content}
