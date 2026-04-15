from pathlib import Path

from langchain_core.documents import Document


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
