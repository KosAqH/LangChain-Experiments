from models import NoteState


def input_node(state: NoteState) -> dict:
    """Validates that topic is present and initializes optional fields."""
    if not state.get("topic", "").strip():
        raise ValueError("Topic is required")

    return {
        "topic": state["topic"].strip(),
        "hints": state.get("hints", "").strip(),
        "source_url": state.get("source_url", None),
        "page_content": None,
        "note": None,
        "flashcards": None,
    }
