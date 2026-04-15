from typing import Any

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from config import OPENROUTER_API_KEY, OPENROUTER_MODEL
from schemas import RagAnswer


def build_chain():
	"""Build a structured-output answer chain."""
	llm = ChatOpenAI(
		model=OPENROUTER_MODEL,
		temperature=0,
		api_key=OPENROUTER_API_KEY,
		base_url="https://openrouter.ai/api/v1",
	)
	structured_llm = llm.with_structured_output(RagAnswer)

	prompt = ChatPromptTemplate.from_template(
		"""
You are a Python docs assistant.
Use ONLY the provided context from local Python documentation to answer.
Assume, that the question is about Python 3.14 unless specified otherwise.
If you can't find the answer, say you don't know.
Return a concise answer and list only sources that directly support the answer.
For every source generate url based on source path like this: library/datetime.txt -> https://docs.python.org/3.14/library/datetime.html
Every source must be from the provided context.

Question:
{question}

Context:
{context}
""".strip()
	)

	return prompt | structured_llm


def coerce_answer_obj(result: Any) -> RagAnswer:
	"""Defensive conversion in case a provider returns dict-like structured data."""
	if isinstance(result, RagAnswer):
		return result
	if isinstance(result, dict):
		return RagAnswer.model_validate(result)
	raise TypeError(f"Unexpected structured output type: {type(result).__name__}")
