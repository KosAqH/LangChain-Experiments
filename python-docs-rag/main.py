import os
import re
from pathlib import Path

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.retrievers import BaseRetriever
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv


BASE_DIR = Path(__file__).parent
DOCS_DIR = BASE_DIR / "data" / "python-3.14-docs-text"
VECTORSTORE_DIR = BASE_DIR / "data" / "faiss_python_docs"
DOCS_BASE_URL = "https://docs.python.org/3.14"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 120
SCORE_BOOST_MODULE_MATCH = 6.0
SCORE_BOOST_SOURCE_MATCH = 2.0
SCORE_BOOST_CONTENT_MATCH = 1.0

load_dotenv(dotenv_path=BASE_DIR / ".env")

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")


class DataLoader:
	"""Loads Python documentation files into LangChain Document objects."""
	
	def __init__(self, docs_dir: Path, base_url: str):
		self.docs_dir = docs_dir
		self.base_url = base_url
	
	def load(self) -> list[Document]:
		"""Load all .txt docs into LangChain Document objects."""
		docs: list[Document] = []
		for path in self.docs_dir.rglob("*.txt"):
			rel_path = path.relative_to(self.docs_dir)
			source = str(rel_path).replace("\\", "/")
			url = f"{self.base_url}/{source[:-4]}.html"
			text = path.read_text(encoding="utf-8", errors="ignore").strip()
			if not text:
				continue
			docs.append(
				Document(
					page_content=text,
					metadata={"source": source, "url": url},
				)
			)
		return docs


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
	
	def build(self, docs: list[Document]) -> None:
		"""Build the dense retriever from documents."""
		splitter = RecursiveCharacterTextSplitter(
			chunk_size=self.chunk_size,
			chunk_overlap=self.chunk_overlap,
			separators=["\n\n", "\n", ". ", " ", ""],
		)

		embeddings = HuggingFaceEmbeddings(
			model_name=self.embedding_model,
			encode_kwargs={"normalize_embeddings": True},
		)

		rebuild_index = os.getenv("REBUILD_VECTORSTORE", "0") == "1"
		if not rebuild_index and self.vectorstore_dir.exists():
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
			print(f"  [{i}] {doc.metadata.get('source', 'unknown')}, {score}, {doc.page_content[:100].replace(chr(10), ' ')}...")
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

		# Reward precise module pages when query mentions a likely module name.
		source_boost = 0.0
		for term in focus:
			if f"library/{term}.txt" in source:
				source_boost += self.score_boost_module_match
			elif term in source:
				source_boost += self.score_boost_source_match

		# Small bonus when focus terms are explicitly mentioned in content.
		content_boost = sum(self.score_boost_content_match for term in focus if term in content)

		# Penalize broad table-of-contents style pages that frequently dominate BM25.
		source_penalty = 1.0 if source.endswith("index.txt") or source == "contents.txt" else 0.0
		primary = float(overlap) + source_boost + content_boost - source_penalty
		secondary = float(overlap) + content_boost
		return (primary, secondary)


class AnswerFormatter:
	"""Formats and processes LLM answers."""
	
	def format_context(self, docs: list[Document]) -> str:
		"""Format documents into a context string."""
		if not docs:
			return "No relevant context found."

		lines: list[str] = []
		for i, doc in enumerate(docs, start=1):
			source = doc.metadata.get("source", "unknown")
			lines.append(f"[{i}] {source}\n{doc.page_content}")
		return "\n\n".join(lines)

	def extract_cited_sources(self, answer: str, docs: list[Document]) -> list[tuple[list[int], str, str]]:
		"""Return cited sources grouped by (source, url) with merged [n] indices."""
		if not docs:
			return []

		max_index = len(docs)
		cited_indices = [
			int(match)
			for match in re.findall(r"\[(\d+)\]", answer)
			if 1 <= int(match) <= max_index
		]

		grouped: dict[tuple[str, str], list[int]] = {}
		order: list[tuple[str, str]] = []
		seen_indices: set[int] = set()
		for idx in cited_indices:
			if idx in seen_indices:
				continue
			seen_indices.add(idx)
			doc = docs[idx - 1]
			source = str(doc.metadata.get("source", "unknown"))
			url = str(doc.metadata.get("url", ""))
			key = (source, url)
			if key not in grouped:
				grouped[key] = []
				order.append(key)
			grouped[key].append(idx)

		return [(grouped[key], key[0], key[1]) for key in order]


def build_chain():
	model_name = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
	llm = ChatOpenAI(
		model=model_name,
		temperature=0,
		api_key=os.getenv("OPENROUTER_API_KEY"),
		base_url="https://openrouter.ai/api/v1",
	)

	prompt = ChatPromptTemplate.from_template(
		"""
You are a Python docs assistant.
Use ONLY the provided context from local Python documentation to answer.
Assume, that the question is about Python 3.14 unless specified otherwise.
If you can't find the answer, say you don't know.
Always include source references like [1] - faq/programming, [2] - library/argparse.
Only cite sources that directly support your answer.

Question:
{question}

Context:
{context}
""".strip()
	)

	chain = prompt | llm | StrOutputParser()
	return chain


def main() -> None:
	if not os.getenv("OPENROUTER_API_KEY"):
		raise RuntimeError("Set OPENROUTER_API_KEY before running this script.")

	if not DOCS_DIR.exists():
		raise FileNotFoundError(f"Docs folder not found: {DOCS_DIR}")

	loader = DataLoader(docs_dir=DOCS_DIR, base_url=DOCS_BASE_URL)
	docs = loader.load()
	if not docs:
		raise RuntimeError(f"No .txt documents loaded from: {DOCS_DIR}")

	retriever = DataRetriever(
		vectorstore_dir=VECTORSTORE_DIR,
		embedding_model=EMBEDDING_MODEL,
	)
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
		answer = chain.invoke({"question": question, "context": context})
		sources = formatter.extract_cited_sources(answer, retrieved_docs)
		print(f"\nAnswer:\n{answer}")
		if sources:
			print("\nSources cited in answer:")
			for indices, source, url in sources:
				index_label = ",".join(str(idx) for idx in indices)
				if url:
					print(f"  [{index_label}] {source} -> {url}")
				else:
					print(f"  [{index_label}] {source}")


if __name__ == "__main__":
	main()
