import logging
import dotenv

dotenv.load_dotenv()

from langgraph.types import Send
from langgraph.graph import END, StateGraph, START

from src.nodes.extract_language import extract_language
from src.nodes.generate_categories import generate_categories
from src.nodes.human_review_categories import human_review_categories
from src.nodes.plan_distribution import plan_distribution
from src.nodes.generate_words import generate_words
from src.nodes.generate_sentences import generate_sentences
from src.nodes.generate_conversations import generate_conversations
from src.nodes.format_and_save import format_and_save
from src.state import FlashcardState


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def _route_to_card_types(state: FlashcardState):
    sends = []
    limits = state.get("card_limits", {})
    for cat in state["categories"]:
        cat_limits = limits.get(cat, {})
        sends.append(Send("generate_words", {
            "category": cat,
            "target_language": state["target_language"],
            "topic_context": state["topic_context"],
            "limit": cat_limits.get("word"),
        }))
        sends.append(Send("generate_sentences", {
            "category": cat,
            "target_language": state["target_language"],
            "topic_context": state["topic_context"],
            "limit": cat_limits.get("sentence"),
        }))
        sends.append(Send("generate_conversations", {
            "category": cat,
            "target_language": state["target_language"],
            "topic_context": state["topic_context"],
            "limit": cat_limits.get("conversation"),
        }))
    return sends


builder = StateGraph(FlashcardState)
builder.add_node("extract_language", extract_language)
builder.add_node("generate_categories", generate_categories)
builder.add_node("human_review_categories", human_review_categories)
builder.add_node("plan_distribution", plan_distribution)
builder.add_node("generate_words", generate_words)
builder.add_node("generate_sentences", generate_sentences)
builder.add_node("generate_conversations", generate_conversations)
builder.add_node("format_and_save", format_and_save)

builder.add_edge(START, "extract_language")
builder.add_edge("extract_language", "generate_categories")
builder.add_edge("generate_categories", "human_review_categories")
builder.add_edge("human_review_categories", "plan_distribution")
builder.add_conditional_edges(
    "plan_distribution", _route_to_card_types, ["generate_words", "generate_sentences", "generate_conversations"]
)
builder.add_edge(["generate_words", "generate_sentences", "generate_conversations"], "format_and_save")
builder.add_edge("format_and_save", END)

graph = builder.compile()


def run(prompt: str) -> dict:
    initial: FlashcardState = {
        "user_prompt": prompt,
        "target_language": "",
        "topic_context": "",
        "max_cards": None,
        "categories": [],
        "card_limits": {},
        "flashcards": [],
        "output_file": "",
    }
    return graph.invoke(initial)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python main.py <prompt>")
        print('Example: python main.py "basic italian"')
        sys.exit(1)

    user_prompt = " ".join(sys.argv[1:])
    logger.info("Starting flashcard generation for: %s", user_prompt)
    result = run(user_prompt)
    logger.info("Done! Flashcards saved to: %s", result["output_file"])
