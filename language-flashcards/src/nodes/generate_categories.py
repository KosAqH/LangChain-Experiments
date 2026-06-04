import logging
from typing import cast
from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter
from src.models import CategoriesResponse
from src.prompts.generate_categories import CATEGORIES_PROMPT
from src.state import FlashcardState


logger = logging.getLogger(__name__)

load_dotenv()

model = ChatOpenRouter(
    model="openai/gpt-4o-mini",
    temperature=0,
)


def generate_categories(state: FlashcardState) -> dict:
    language = state["target_language"]
    topic = state["topic_context"]
    logger.info("Generating categories for %s — %s", language, topic)
    prompt = CATEGORIES_PROMPT.format(language=language, topic=topic)
    response = cast(CategoriesResponse, model.with_structured_output(CategoriesResponse).invoke(prompt))
    logger.info("Generated %d categories: %s", len(response.categories), response.categories)
    return {"categories": response.categories}
