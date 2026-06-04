from typing import TypedDict, Optional, Annotated
import operator


class FlashcardState(TypedDict):
    user_prompt: str
    target_language: str
    topic_context: str
    max_cards: Optional[int]
    categories: list[str]
    flashcards: Annotated[list[dict], operator.add]
    output_file: str


class CategoryCardTypeState(TypedDict):
    category: str
    target_language: str
    topic_context: str
    max_cards: Optional[int]
    flashcards: list[dict]
