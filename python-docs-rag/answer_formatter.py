from langchain_core.documents import Document

from schemas import RagAnswer


class AnswerFormatter:
    """Formats context and normalizes sources from structured answers."""

    def format_context(self, docs: list[Document]) -> str:
        """Format documents into a context string."""
        if not docs:
            return "No relevant context found."

        lines: list[str] = []
        for i, doc in enumerate(docs, start=1):
            source = doc.metadata.get("source", "unknown")
            lines.append(f"[{i}] {source}\n{doc.page_content}")
        return "\n\n".join(lines)

    def normalize_sources(
        self, answer: RagAnswer
    ) -> list[tuple[str, str]]:
        """Keep only complete source-url entries and remove duplicates."""
        seen = set()

        for item in answer.sources:
            source = item.source.strip()
            url = item.url.strip()

            if not source or not url:
                continue

            candidate = (source, url)
            if candidate in seen:
                continue
            seen.add(candidate)

        return list(seen)
