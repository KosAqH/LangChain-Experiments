import logging
from typing import cast
from src.llm import model
from src.models import ExtractedPrompt
from src.prompts.extract_language import EXTRACT_PROMPT
from src.state import FlashcardState


logger = logging.getLogger(__name__)


def extract_language(state: FlashcardState) -> dict:
    user_prompt = state["user_prompt"]
    logger.info("Extracting language and topic from prompt: %s", user_prompt)
    prompt = EXTRACT_PROMPT.format(user_prompt=user_prompt)
    response = cast(
        ExtractedPrompt, model.with_structured_output(ExtractedPrompt).invoke(prompt)
    )
    logger.info(
        "Detected language=%s, topic=%s, max_cards=%s",
        response.language,
        response.topic,
        response.max_cards,
    )
    return {
        "target_language": response.language,
        "topic_context": response.topic,
        "max_cards": response.max_cards,
    }
