import logging
from typing import cast
from src.llm import model
from src.models import CategoryConversationFlashcards
from src.prompts.generate_conversations import FLASHCARDS_CONVERSATIONS_PROMPT
from src.state import CategoryCardTypeState


logger = logging.getLogger(__name__)


def generate_conversations(state: CategoryCardTypeState) -> dict:
    language = state["target_language"]
    topic = state["topic_context"]
    category = state["category"]
    logger.info("Generating conversation flashcards for category: %s", category)
    prompt = FLASHCARDS_CONVERSATIONS_PROMPT.format(
        language=language,
        topic=topic,
        category=category,
    )
    response = cast(
        CategoryConversationFlashcards,
        model.with_structured_output(CategoryConversationFlashcards).invoke(prompt),
    )
    cards = [f.model_dump() for f in response.flashcards]
    logger.info(
        "Generated %d conversation flashcards for category: %s", len(cards), category
    )
    return {"flashcards": cards}
