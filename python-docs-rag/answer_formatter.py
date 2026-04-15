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

	def normalize_sources(self, answer: RagAnswer, docs: list[Document]) -> list[tuple[str, str]]:
		"""Map model-provided sources to retrieved docs, allowing source-only/url-only entries."""
		doc_pairs = [
			(str(doc.metadata.get("source", "")), str(doc.metadata.get("url", "")))
			for doc in docs
		]
		by_source = {source: url for source, url in doc_pairs if source}
		by_url = {url: source for source, url in doc_pairs if url}

		normalized: list[tuple[str, str]] = []
		seen: set[tuple[str, str]] = set()
		for item in answer.sources:
			source = item.source.strip()
			url = item.url.strip()

			if source and not url:
				url = by_source.get(source, "")
			if url and not source:
				source = by_url.get(url, "")
			if source and source in by_source:
				url = by_source[source]
			elif url and url in by_url:
				source = by_url[url]
			else:
				continue

			candidate = (source, url)
			if candidate in seen:
				continue
			seen.add(candidate)
			normalized.append(candidate)

		return normalized
