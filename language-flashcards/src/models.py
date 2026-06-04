from typing import Literal
from pydantic import BaseModel


class ExtractedPrompt(BaseModel):
    language: str
    topic: str
    max_cards: int | None = None


class CategoriesResponse(BaseModel):
    categories: list[str]


class FlashcardBase(BaseModel):
    category: str
    type: Literal["word", "sentence", "conversation"]
    front_en: str
    back_foreign: str
    pronunciation_en: str
    pronunciation_phonetic: str


class Flashcard(FlashcardBase):
    example_en: str = ""
    example_foreign: str = ""


class CategoryWordFlashcards(BaseModel):
    category: str
    flashcards: list[Flashcard]


class CategorySentenceFlashcards(BaseModel):
    category: str
    flashcards: list[FlashcardBase]


class CategoryConversationFlashcards(BaseModel):
    category: str
    flashcards: list[FlashcardBase]
