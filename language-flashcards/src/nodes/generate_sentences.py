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
    prompt = FLASHCARDS_SENTENCES_PROMPT.format(
        language=language,
        topic=topic,
        category=category,
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
