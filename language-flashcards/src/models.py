from typing import Optional, Literal
from pydantic import BaseModel


class ExtractedPrompt(BaseModel):
    language: str
    topic: str
    max_cards: Optional[int] = None


class CategoriesResponse(BaseModel):
    categories: list[str]


class Flashcard(BaseModel):
    category: str
    type: Literal["word", "sentence", "conversation"]
    front_en: str
    back_foreign: str
    pronunciation_en: str
    pronunciation_phonetic: str
    example_en: Optional[str] = None
    example_foreign: Optional[str] = None


class CategoryFlashcards(BaseModel):
    category: str
    flashcards: list[Flashcard]
