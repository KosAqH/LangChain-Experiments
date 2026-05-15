from typing import TypedDict


class NoteState(TypedDict):
    query: str
    topic: str
    hints: str
    source_urls: list[str]
    page_content: str | None
    note: str | None
    flashcards: str | None
