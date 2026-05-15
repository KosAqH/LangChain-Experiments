from langgraph.graph import StateGraph, END
from models import NoteState
from nodes.input import input_node
from nodes.url_resolver import url_resolver_node
from nodes.loader import loader_node
from nodes.note_maker import note_maker_node
from nodes.flashcard_maker import flashcard_maker_node
from nodes.storage import storage_node


def build_graph():
    graph = StateGraph(NoteState)

    graph.add_node("input", input_node)
    graph.add_node("url_resolver", url_resolver_node)
    graph.add_node("loader", loader_node)
    graph.add_node("note_maker", note_maker_node)
    graph.add_node("flashcard_maker", flashcard_maker_node)
    graph.add_node("storage", storage_node)

    graph.set_entry_point("input")
    graph.add_edge("input", "url_resolver")
    graph.add_edge("url_resolver", "loader")
    graph.add_edge("loader", "note_maker")
    graph.add_edge("note_maker", "flashcard_maker")
    graph.add_edge("flashcard_maker", "storage")
    graph.add_edge("storage", END)

    return graph.compile()
