from __future__ import annotations

import importlib
import os
import re
from pathlib import Path

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.retrievers import BaseRetriever
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


BASE_DIR = Path(__file__).parent
DOCS_DIR = BASE_DIR / "data" / "python-3.14-docs-text"


load_dotenv(dotenv_path=BASE_DIR / ".env")


def load_python_docs(docs_dir: Path) -> list[Document]:
	"""Load all .txt docs into LangChain Document objects."""
	docs: list[Document] = []
	for path in docs_dir.rglob("*.txt"):
		text = path.read_text(encoding="utf-8", errors="ignore").strip()
		if not text:
			continue
		docs.append(
			Document(
				page_content=text,
				metadata={"source": str(path.relative_to(docs_dir))},
			)
		)
	return docs


def build_dense_retriever(docs: list[Document]) -> BaseRetriever:
	splitter = RecursiveCharacterTextSplitter(
		chunk_size=800,
		chunk_overlap=120,
		separators=["\n\n", "\n", ". ", " ", ""],
	)
	chunks = splitter.split_documents(docs)
	faiss_mod = importlib.import_module("langchain_community.vectorstores")
	hf_mod = importlib.import_module("langchain_huggingface")
	FAISS = getattr(faiss_mod, "FAISS")
	HuggingFaceEmbeddings = getattr(hf_mod, "HuggingFaceEmbeddings")

	embedding_model = os.getenv(
		"EMBEDDING_MODEL",
		"sentence-transformers/all-MiniLM-L6-v2",
	)
	embeddings = HuggingFaceEmbeddings(
		model_name=embedding_model,
		encode_kwargs={"normalize_embeddings": True},
	)
	vector_store = FAISS.from_documents(chunks, embeddings)
	print(f"Dense retrieval enabled with model: {embedding_model}")
	return vector_store.as_retriever(search_kwargs={"k": 40})


def _tokenize(text: str) -> set[str]:
	return set(re.findall(r"[a-zA-Z_][a-zA-Z0-9_\-]{1,}", text.lower()))


def _focus_terms(question: str) -> list[str]:
	"""Extract lexical terms from a question for reranking."""
	tokens = sorted(_tokenize(question))
	return [t for t in tokens if len(t) >= 3]


def retrieve_relevant_docs(
	question: str,
	dense_retriever: BaseRetriever,
) -> list[Document]:
	"""Retrieve with dense embeddings, then rerank by lexical overlap and source quality."""
	candidates_by_key: dict[tuple[str, int], Document] = {}
	try:
		for doc in dense_retriever.invoke(question):
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

	q_tokens = _tokenize(question)
	focus = _focus_terms(question)

	def score(doc: Document) -> tuple[float, float]:
		source = str(doc.metadata.get("source", "")).lower()
		content = doc.page_content.lower()
		d_tokens = _tokenize(content)
		overlap = len(q_tokens & d_tokens)

		# Reward precise module pages when query mentions a likely module name.
		source_boost = 0.0
		for term in focus:
			if f"library/{term}.txt" in source:
				source_boost += 6.0
			elif term in source:
				source_boost += 2.0

		# Small bonus when focus terms are explicitly mentioned in content.
		content_boost = sum(1.0 for term in focus if term in content)

		# Penalize broad table-of-contents style pages that frequently dominate BM25.
		source_penalty = 1.0 if source.endswith("index.txt") or source == "contents.txt" else 0.0
		primary = float(overlap) + source_boost + content_boost - source_penalty
		secondary = float(overlap) + content_boost
		return (primary, secondary)

	reranked = sorted(candidates, key=score, reverse=True)
	print(f"Retrieved {len(candidates)} dense candidates, reranked top 8:")
	for i, doc in enumerate(reranked[:8], start=1):
		print(f"  [{i}] {doc.metadata.get('source', 'unknown')}")
	return reranked[:8]


def format_context(docs: list[Document]) -> str:
	if not docs:
		return "No relevant context found."

	lines: list[str] = []
	for i, doc in enumerate(docs, start=1):
		source = doc.metadata.get("source", "unknown")
		lines.append(f"[{i}] {source}\n{doc.page_content}")
	return "\n\n".join(lines)


def build_chain(dense_retriever: BaseRetriever):
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

Question:
{question}

Context:
{context}
""".strip()
	)

	chain = (
		{
			"context": RunnableLambda(lambda q: retrieve_relevant_docs(q, dense_retriever)) | format_context,
			"question": RunnablePassthrough(),
		}
		| prompt
		| llm
		| StrOutputParser()
	)
	return chain


def main() -> None:
	if not os.getenv("OPENROUTER_API_KEY"):
		raise RuntimeError("Set OPENROUTER_API_KEY before running this script.")

	if not DOCS_DIR.exists():
		raise FileNotFoundError(f"Docs folder not found: {DOCS_DIR}")

	docs = load_python_docs(DOCS_DIR)
	if not docs:
		raise RuntimeError(f"No .txt documents loaded from: {DOCS_DIR}")

	dense_retriever = build_dense_retriever(docs)
	chain = build_chain(dense_retriever)

	print("Python Docs RAG is ready. Type 'exit' to quit.")
	while True:
		question = input("\nQuestion: ").strip()
		if not question or question.lower() in {"exit", "quit"}:
			print("Bye.")
			break

		answer = chain.invoke(question)
		print(f"\nAnswer:\n{answer}")


if __name__ == "__main__":
	main()
