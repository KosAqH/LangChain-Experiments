# Python Docs RAG

A Retrieval-Augmented Generation (RAG) system that provides intelligent access to Python documentation using LangChain and FAISS vector search.

## Description

This project implements a production-ready RAG pipeline that:

- **Indexes** Python 3.14 documentation into a FAISS vector store for fast similarity search
- **Retrieves** relevant documentation sections based on natural language queries
- **Augments** responses by combining retrieved context with LLM reasoning
- Uses **HuggingFace embeddings** for semantic understanding
- Integrates with **OpenAI** for intelligent response generation
- Provides **source tracking** with direct links to official Python docs

### Key Features

- Chunked document processing with configurable overlap for better context preservation
- Score boosting for improved relevance (module matching, source relevance, content matching)
- Vector similarity search via FAISS for sub-millisecond retrieval
- Direct hyperlinks to official Python documentation
- Full support for Python standard library and C API documentation

## Setup

### Prerequisites

- Python 3.13+
- OpenAI or OpenRouter API key
- Parent project setup completed (see [../../README.md](../../README.md))

### Installation

1. **From the project root**, install the main dependencies:

   ```bash
   uv sync
   ```
2. ```bash
   cp .env.example .env
   ```
3. **Set your OpenAI API key** in `.env`:

   ```
   OPENAI_API_KEY=sk-...
   EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
   ```

### Data Setup

#### Downloading Python Documentation (Text Version)

1. **Create the data directory**:
   ```bash
   mkdir -p python-docs-rag/data
   cd python-docs-rag/data
   ```

2. **Download Python 3.14 text documentation**:
   ```bash
   # Download the text version (.tar.bz2)
   wget https://docs.python.org/3.14/archives/python-3.14-docs-text.tar.bz2
   
   # Or on Windows with curl:
   curl -O https://docs.python.org/3.14/archives/python-3.14-docs-text.tar.bz2
   ```

3. **Extract the archive**:
   ```bash
   # On Linux/Mac:
   tar -xjf python-3.14-docs-text.tar.bz2
   
   # On Windows (using PowerShell with 7z or WSL):
   7z x python-3.14-docs-text.tar.bz2
   tar -xf python-3.14-docs-text.tar
   ```

4. **Verify structure**:
   ```
   data/
   ├── python-3.14-docs-text/     # Text documentation files
   │   ├── about.txt
   │   ├── library/
   │   ├── c-api/
   │   └── ...
   └── python-3.14-docs-text-slim/ # Optional: condensed version
   ```

#### FAISS Vector Store

The vector store is **automatically generated** on first run:

```bash
uv run python-docs-rag/main.py
```

This will:
- Load all `.txt` files from `data/python-3.14-docs-text/`
- Create embeddings using the configured embedding model
- Build and save the FAISS index to `data/faiss_python_docs/`
- First run may take 5-15 minutes depending on document size

To **rebuild** the vector store:
```bash
rm -r data/faiss_python_docs/
uv run python-docs-rag/main.py
```

#### Directory Structure

- **`data/python-3.14-docs-text/`**: Raw Python documentation (.txt files)
- **`data/faiss_python_docs/`**: FAISS vector store index (auto-generated)
- **`data/python-3.14-docs-text-slim/`**: Optional condensed version for testing
- **`storage/`**: Processed documents and metadata

## Usage

### Running the Main Script

```bash
uv run python-docs-rag/main.py
```

This will:

1. Load Python documentation files
2. Build or load the FAISS vector store
3. Create a retriever pipeline
4. Set up the LangChain RAG chain
5. Process queries against the documentation

### Configuration

Edit parameters in `main.py`:

- `CHUNK_SIZE`: Document split size (default: 800 tokens)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 120 tokens)
- `SCORE_BOOST_*`: Weights for relevance scoring
- `EMBEDDING_MODEL`: HuggingFace model for embeddings

## Architecture

```
Query
  ↓
Embedding (HuggingFace)
  ↓
FAISS Similarity Search
  ↓
Retrieved Documents (with ranking)
  ↓
LLM Prompt + Retrieved Context
  ↓
Augmented Response
```

## Dependencies

- **langchain**: Core RAG framework
- **faiss-cpu**: Vector similarity search
- **sentence-transformers**: Semantic embeddings
- **langchain-openai**: OpenAI LLM integration
- **langchain-huggingface**: HuggingFace embedding integration
- **langchain-text-splitters**: Document chunking

## Troubleshooting

- **FAISS index errors**: Delete `data/faiss_python_docs/` to rebuild
