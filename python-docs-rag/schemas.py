from pydantic import BaseModel, Field


class UsedSource(BaseModel):
    """Single source used by the assistant."""

    source: str = Field(
        description="Relative source file path, e.g. library/datetime.txt"
    )
    url: str = Field(default="", description="Source URL")


class RagAnswer(BaseModel):
    """Structured RAG answer returned by the LLM."""

    message: str = Field(description="Final answer for the user")
    sources: list[UsedSource] = Field(
        default_factory=list, description="Sources supporting the answer"
    )
