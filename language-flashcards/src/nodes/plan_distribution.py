import logging
from typing import cast
from src.llm import model
from src.models import DistributionPlan
from src.prompts.plan_distribution import PLAN_DISTRIBUTION_PROMPT
from src.state import FlashcardState


logger = logging.getLogger(__name__)


def plan_distribution(state: FlashcardState) -> dict:
    language = state["target_language"]
    topic = state["topic_context"]
    max_cards = state.get("max_cards")

    if max_cards is None:
        logger.info("No max_cards set, skipping distribution planning")
        return {"card_limits": {}}

    categories = state["categories"]
    logger.info("Planning distribution of %d cards across %d categories", max_cards, len(categories))

    prompt = PLAN_DISTRIBUTION_PROMPT.format(
        language=language,
        topic=topic,
        max_cards=max_cards,
        categories=", ".join(categories),
    )
    response = cast(
        DistributionPlan,
        model.with_structured_output(DistributionPlan).invoke(prompt),
    )

    card_limits: dict[str, dict[str, int]] = {}
    for entry in response.distribution:
        cat = entry.category
        if cat not in card_limits:
            card_limits[cat] = {}
        card_limits[cat][entry.type] = entry.limit

    logger.info("Distribution plan: %s", card_limits)
    return {"card_limits": card_limits}
