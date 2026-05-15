from langchain_openrouter import ChatOpenRouter
from prompts import FLASHCARD_SYSTEM_PROMPT
from models import NoteState


def flashcard_maker_node(state: NoteState) -> dict:
    """Generates Anki-formatted flashcards from the note."""
    llm = ChatOpenRouter(model="openai/gpt-4o-mini")

    messages = [
        ("system", FLASHCARD_SYSTEM_PROMPT),
        ("human", state["note"]),
    ]

    response = llm.invoke(messages)

    return {"flashcards": response.content}
