import re
from pathlib import Path

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from config import (
	CHUNK_OVERLAP,
	CHUNK_SIZE,
	REBUILD_VECTORSTORE,
	SCORE_BOOST_CONTENT_MATCH,
	SCORE_BOOST_MODULE_MATCH,
	SCORE_BOOST_SOURCE_MATCH,
)


class DataRetriever:
	"""Manages dense vector retrieval and reranking of documents."""

	def __init__(
		self,
		vectorstore_dir: Path,
		embedding_model: str,
		chunk_size: int = CHUNK_SIZE,
		chunk_overlap: int = CHUNK_OVERLAP,
		retriever_k: int = 20,
		score_boost_module_match: float = SCORE_BOOST_MODULE_MATCH,
		score_boost_source_match: float = SCORE_BOOST_SOURCE_MATCH,
		score_boost_content_match: float = SCORE_BOOST_CONTENT_MATCH,
	):
		self.vectorstore_dir = vectorstore_dir
		self.embedding_model = embedding_model
		self.chunk_size = chunk_size
		self.chunk_overlap = chunk_overlap
		self.retriever_k = retriever_k
		self.score_boost_module_match = score_boost_module_match
		self.score_boost_source_match = score_boost_source_match
		self.score_boost_content_match = score_boost_content_match
		self.retriever: BaseRetriever | None = None

	def build(self, docs: list[Document] | None = None) -> None:
		"""Load persisted dense retriever or build it from documents."""
		embeddings = HuggingFaceEmbeddings(
			model_name=self.embedding_model,
			encode_kwargs={"normalize_embeddings": True},
		)

		if not REBUILD_VECTORSTORE and self.vectorstore_dir.exists():
			try:
				vector_store = FAISS.load_local(
					str(self.vectorstore_dir),
					embeddings,
					allow_dangerous_deserialization=True,
				)
				self.retriever = vector_store.as_retriever(search_kwargs={"k": self.retriever_k})
				print(f"Loaded persisted vector store from: {self.vectorstore_dir}")
				print(f"Dense retrieval enabled with model: {self.embedding_model}")
				return
			except Exception as exc:
				print(f"Failed to load persisted vector store, rebuilding: {exc}")

		if not docs:
			raise RuntimeError(
				"No documents provided to build retriever. "
				"Set REBUILD_VECTORSTORE=1 or provide docs when no persisted index is available."
			)

		splitter = RecursiveCharacterTextSplitter(
			chunk_size=self.chunk_size,
			chunk_overlap=self.chunk_overlap,
			separators=["\n\n", "\n", ". ", " ", ""],
		)
		chunks = splitter.split_documents(docs)
		vector_store = FAISS.from_documents(chunks, embeddings)
		self.vectorstore_dir.mkdir(parents=True, exist_ok=True)
		vector_store.save_local(str(self.vectorstore_dir))
		self.retriever = vector_store.as_retriever(search_kwargs={"k": self.retriever_k})
		print(f"Persisted vector store saved to: {self.vectorstore_dir}")
		print(f"Dense retrieval enabled with model: {self.embedding_model}")

	def retrieve(self, question: str) -> list[Document]:
		"""Retrieve with dense embeddings, then rerank by lexical overlap and source quality."""
		if self.retriever is None:
			raise RuntimeError("Retriever not built. Call build() first.")

		candidates_by_key: dict[tuple[str, int], Document] = {}
		try:
			for doc in self.retriever.invoke(question):
				source = str(doc.metadata.get("source", ""))
				key = (source, hash(doc.page_content))
				if key not in candidates_by_key:
					candidates_by_key[key] = doc
		except Exception as exc:
			print(f"Dense retrieval query failed: {exc}")
			return []

		candidates = list(candidates_by_key.values())
		if not candidates:
			return []

		q_tokens = self._tokenize(question)
		focus = self._focus_terms(question)

		reranked = sorted(candidates, key=lambda doc: self._score(doc, q_tokens, focus), reverse=True)
		print(f"Retrieved {len(candidates)} dense candidates, reranked top 8:")
		for i, doc in enumerate(reranked[:8], start=1):
			score = self._score(doc, q_tokens, focus)
			preview = doc.page_content[:100].replace(chr(10), " ")
			print(f"  [{i}] {doc.metadata.get('source', 'unknown')}, {score}, {preview}...")
		return reranked[:8]

	def _tokenize(self, text: str) -> set[str]:
		"""Extract tokens from text."""
		return set(re.findall(r"[a-zA-Z_][a-zA-Z0-9_\-]{1,}", text.lower()))

	def _focus_terms(self, question: str) -> list[str]:
		"""Extract lexical terms from a question for reranking."""
		tokens = sorted(self._tokenize(question))
		return [t for t in tokens if len(t) >= 3]

	def _score(self, doc: Document, q_tokens: set[str], focus: list[str]) -> tuple[float, float]:
		"""Score a document based on token overlap and source quality."""
		source = str(doc.metadata.get("source", "")).lower()
		content = doc.page_content.lower()
		d_tokens = self._tokenize(content)
		overlap = len(q_tokens & d_tokens)

		source_boost = 0.0
		for term in focus:
			if f"library/{term}.txt" in source:
				source_boost += self.score_boost_module_match
			elif term in source:
				source_boost += self.score_boost_source_match

		content_boost = sum(self.score_boost_content_match for term in focus if term in content)
		source_penalty = 1.0 if source.endswith("index.txt") or source == "contents.txt" else 0.0
		primary = float(overlap) + source_boost + content_boost - source_penalty
		secondary = float(overlap) + content_boost
		return (primary, secondary)
