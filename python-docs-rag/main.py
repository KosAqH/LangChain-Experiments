from langchain_core.documents import Document

from answer_formatter import AnswerFormatter
from chain_builder import build_chain, coerce_answer_obj
from config import (
    DOCS_BASE_URL,
    DOCS_DIR,
    EMBEDDING_MODEL,
    OPENROUTER_API_KEY,
    REBUILD_VECTORSTORE,
    VECTORSTORE_DIR,
)
from data_loader import DataLoader
from retriever import DataRetriever


def main() -> None:
    """Run the interactive Python docs RAG CLI."""
    if not OPENROUTER_API_KEY:
        raise RuntimeError("Set OPENROUTER_API_KEY before running this script.")

    retriever = DataRetriever(
        vectorstore_dir=VECTORSTORE_DIR,
        embedding_model=EMBEDDING_MODEL,
    )

    docs: list[Document] | None = None
    if REBUILD_VECTORSTORE or not VECTORSTORE_DIR.exists():
        if not DOCS_DIR.exists():
            raise FileNotFoundError(f"Docs folder not found: {DOCS_DIR}")

        loader = DataLoader(docs_dir=DOCS_DIR, base_url=DOCS_BASE_URL)
        docs = loader.load()
        if not docs:
            raise RuntimeError(f"No .txt documents loaded from: {DOCS_DIR}")

    retriever.build(docs)
    formatter = AnswerFormatter()
    chain = build_chain()

    print("Python Docs RAG is ready. Type 'exit' to quit.")
    while True:
        question = input("\nQuestion: ").strip()
        if not question or question.lower() in {"exit", "quit"}:
            print("Bye.")
            break

        retrieved_docs = retriever.retrieve(question)
        context = formatter.format_context(retrieved_docs)
        result = chain.invoke({"question": question, "context": context})
        answer = coerce_answer_obj(result)
        sources = formatter.normalize_sources(answer, retrieved_docs)

        print(f"\nAnswer:\n{answer.message.strip()}")
        if sources:
            print("\nSources used:")
            for source, url in sources:
                if url:
                    print(f"  - {source} -> {url}")
                else:
                    print(f"  - {source}")


if __name__ == "__main__":
    main()
