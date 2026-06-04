import logging
import dotenv

from langgraph.types import Send
from langgraph.graph import END, StateGraph, START

from src.nodes.extract_language import extract_language
from src.nodes.generate_categories import generate_categories
from src.nodes.generate_flashcards import generate_flashcards
from src.nodes.format_and_save import format_and_save
from src.state import FlashcardState


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

dotenv.load_dotenv()


def _route_to_categories(state: FlashcardState):
    return [
        Send(
            "generate_flashcards",
            {
                "category": cat,
                "target_language": state["target_language"],
                "topic_context": state["topic_context"],
                "max_cards": state.get("max_cards"),
            },
        )
        for cat in state["categories"]
    ]


builder = StateGraph(FlashcardState)
builder.add_node("extract_language", extract_language)
builder.add_node("generate_categories", generate_categories)
builder.add_node("generate_flashcards", generate_flashcards)
builder.add_node("format_and_save", format_and_save)

builder.add_edge(START, "extract_language")
builder.add_edge("extract_language", "generate_categories")
builder.add_conditional_edges(
    "generate_categories", _route_to_categories, ["generate_flashcards"]
)
builder.add_edge("generate_flashcards", "format_and_save")
builder.add_edge("format_and_save", END)

graph = builder.compile()


def run(prompt: str) -> dict:
    initial: FlashcardState = {
        "user_prompt": prompt,
        "target_language": "",
        "topic_context": "",
        "max_cards": None,
        "categories": [],
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
