import os
from pathlib import Path

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
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
REBUILD_VECTORSTORE = os.getenv("REBUILD_VECTORSTORE", "0") == "1"
