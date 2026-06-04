from typing import cast
from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter
from src.models import CategoryFlashcards
from src.prompts.generate_flashcards import FLASHCARDS_PROMPT
from src.state import CategoryState


load_dotenv()

model = ChatOpenRouter(
    model="openai/gpt-4o-mini",
    temperature=0,
)


def generate_flashcards(state: CategoryState) -> dict:
    language = state["target_language"]
    topic = state["topic_context"]
    category = state["category"]
    prompt = FLASHCARDS_PROMPT.format(
        language=language,
        topic=topic,
        category=category,
    )
    response = cast(
        CategoryFlashcards,
        model.with_structured_output(CategoryFlashcards).invoke(prompt),
    )
    return {"flashcards": [f.model_dump() for f in response.flashcards]}
