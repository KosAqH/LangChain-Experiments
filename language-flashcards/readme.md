# Language Flashcards Generator

Generates Anki-ready flashcards for any language using LLM-powered LangGraph workflows.

## Setup

```bash
# Install dependencies (from workspace root)
uv sync

# Configure environment
cp .env.example .env
# Edit .env and add your OPENROUTER_API_KEY
```

## Usage

```bash
python main.py "basic italian"
python main.py "trip to mountains in slovakia"
python main.py "100 most important french words"
```

Output is saved to `output/` as JSON, CSV, and Anki-import TXT files.

## Import to Anki

1. Open Anki → File → Import
2. Select the `.txt` file from `output/`
3. Set field separator to **Tab**
4. Map fields: Front, Back, Pronunciation EN, Pronunciation IPA, Example EN, Example Foreign, Tags
5. Import

## Project Structure

```
src/
├── state.py              # TypedDict state definitions
├── models.py             # Pydantic models for structured output
├── nodes/
│   ├── extract_language.py
│   ├── generate_categories.py
│   ├── generate_flashcards.py
│   └── format_and_save.py
└── prompts/
    ├── extract_language.py
    ├── generate_categories.py
    └── generate_flashcards.py
```
