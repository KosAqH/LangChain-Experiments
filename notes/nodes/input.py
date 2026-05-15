from langchain_openrouter import ChatOpenRouter
from pydantic import BaseModel, Field
from models import NoteState


class ParsedQuery(BaseModel):
    topic: str = Field(description="The main topic to create a note about")
    hints: str = Field(description="Any hints or structuring guidance, empty string if none")
    source_urls: list[str] = Field(description="List of URLs if provided, empty list if none")


def input_node(state: NoteState) -> dict:
    """Uses LLM to parse a single query string into topic, hints, and optional URLs."""
    query = state.get("query", "").strip()
    if not query:
        raise ValueError("Query is required")

    llm = ChatOpenRouter(model="openai/gpt-4o-mini")
    structured_llm = llm.with_structured_output(ParsedQuery)

    parsed = structured_llm.invoke(
        f"Parse this query into topic, hints, and optional URLs:\n\n{query}"
    )

    return {
        "topic": parsed.topic,
        "hints": parsed.hints,
        "source_urls": parsed.source_urls,
        "page_content": None,
        "note": None,
        "flashcards": None,
    }
