from typing import TypedDict, Optional


class FlashcardState(TypedDict):
    user_prompt: str
    target_language: str
    topic_context: str
    max_cards: Optional[int]
    categories: list[str]
    flashcards: list[dict]
    output_file: str
