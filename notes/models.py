from typing import TypedDict


class NoteState(TypedDict):
    topic: str
    hints: str
    source_url: str | None
    page_content: str | None
    note: str | None
    flashcards: str | None
