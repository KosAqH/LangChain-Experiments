from db import save_note
from models import NoteState


async def storage_node(state: NoteState) -> dict:
    """Persists the note and flashcards to SQLite."""
    resources = [state["source_url"]] if state.get("source_url") else []
    note_id = await save_note(
        topic=state["topic"],
        resources=resources,
        note=state["note"] or "",
        flashcards=state["flashcards"] or "",
    )

    return {"note_id": note_id}
