from typing import Literal
from pydantic import BaseModel


class ExtractedPrompt(BaseModel):
    language: str
    topic: str
    max_cards: int | None = None


class CategoriesResponse(BaseModel):
    categories: list[str]


class Flashcard(BaseModel):
    category: str
    type: Literal["word", "sentence", "conversation"]
    front_en: str
    back_foreign: str
    pronunciation_en: str
    pronunciation_phonetic: str
    example_en: str = ""
    example_foreign: str = ""


class CategoryFlashcards(BaseModel):
    category: str
    flashcards: list[Flashcard]
