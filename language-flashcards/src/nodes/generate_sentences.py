import logging
from typing import cast
from src.llm import model
from src.models import CategorySentenceFlashcards
from src.prompts.generate_sentences import FLASHCARDS_SENTENCES_PROMPT
from src.state import CategoryCardTypeState


logger = logging.getLogger(__name__)


def generate_sentences(state: CategoryCardTypeState) -> dict:
    language = state["target_language"]
    topic = state["topic_context"]
    category = state["category"]
    logger.info("Generating sentence flashcards for category: %s", category)
    limit = state.get("limit")
    if limit is None:
        limit_instruction = "Generate as many high-quality sentence flashcards as are useful for this category."
    else:
        limit_instruction = f"Aim to generate approximately {limit} high-quality sentence flashcards."
    prompt = FLASHCARDS_SENTENCES_PROMPT.format(
        language=language,
        topic=topic,
        category=category,
        limit_instruction=limit_instruction,
    )
    response = cast(
        CategorySentenceFlashcards,
        model.with_structured_output(CategorySentenceFlashcards).invoke(prompt),
    )
    cards = [f.model_dump() for f in response.flashcards]
    logger.info(
        "Generated %d sentence flashcards for category: %s", len(cards), category
    )
    return {"flashcards": cards}
