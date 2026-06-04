import logging
from typing import cast
from src.llm import model
from src.models import CategoryWordFlashcards
from src.prompts.generate_words import FLASHCARDS_WORDS_PROMPT
from src.state import CategoryCardTypeState


logger = logging.getLogger(__name__)


def generate_words(state: CategoryCardTypeState) -> dict:
    language = state["target_language"]
    topic = state["topic_context"]
    category = state["category"]
    logger.info("Generating word flashcards for category: %s", category)
    limit = state.get("limit")
    if limit is None:
        limit_instruction = "Generate as many high-quality word flashcards as are useful for this category."
    else:
        limit_instruction = f"Aim to generate approximately {limit} high-quality word flashcards."
    prompt = FLASHCARDS_WORDS_PROMPT.format(
        language=language,
        topic=topic,
        category=category,
        limit_instruction=limit_instruction,
    )
    response = cast(
        CategoryWordFlashcards,
        model.with_structured_output(CategoryWordFlashcards).invoke(prompt),
    )
    cards = [f.model_dump() for f in response.flashcards]
    logger.info("Generated %d word flashcards for category: %s", len(cards), category)
    return {"flashcards": cards}
