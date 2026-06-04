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
    front_en: str
    back_foreign: str
    pronunciation_en: str
    pronunciation_phonetic: str


class WordFlashcard(FlashcardBase):
    type: Literal["word"] = "word"
    example_en: str = ""
    example_foreign: str = ""


class SentenceFlashcard(FlashcardBase):
    type: Literal["sentence"] = "sentence"


class ConversationFlashcard(FlashcardBase):
    type: Literal["conversation"] = "conversation"


class CategoryWordFlashcards(BaseModel):
    category: str
    flashcards: list[WordFlashcard]


class CategorySentenceFlashcards(BaseModel):
    category: str
    flashcards: list[SentenceFlashcard]


class CategoryConversationFlashcards(BaseModel):
    category: str
    flashcards: list[ConversationFlashcard]


class DistributionEntry(BaseModel):
    category: str
    type: str
    limit: int


class DistributionPlan(BaseModel):
    distribution: list[DistributionEntry]
