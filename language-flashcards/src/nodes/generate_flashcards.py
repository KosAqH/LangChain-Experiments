import logging
from typing import cast
from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter
from src.models import CategoryFlashcards
from src.prompts.generate_flashcards import FLASHCARDS_PROMPT
from src.state import CategoryState


logger = logging.getLogger(__name__)

load_dotenv()

model = ChatOpenRouter(
    model="openai/gpt-4o-mini",
    temperature=0,
)


def generate_flashcards(state: CategoryState) -> dict:
    language = state["target_language"]
    topic = state["topic_context"]
    category = state["category"]
    logger.info("Generating flashcards for category: %s", category)
    prompt = FLASHCARDS_PROMPT.format(
        language=language,
        topic=topic,
        category=category,
    )
    response = cast(
        CategoryFlashcards,
        model.with_structured_output(CategoryFlashcards).invoke(prompt),
    )
    cards = [f.model_dump() for f in response.flashcards]
    logger.info("Generated %d flashcards for category: %s", len(cards), category)
    return {"flashcards": cards}
