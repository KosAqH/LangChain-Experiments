language-flashcards:

- agents.md - contains the code convention and project schema reference for the language flashcards project.
- readme.md - contains the project description, installation instructions, and usage guide for the language flashcards project.
- .env.example - contains an example of the environment variables needed for the project.
- main.py - contains the main code for the language flashcards project, including the implementation of the flashcard generation and review process.
- plan.md - contains the implementation plan for the language flashcards project.
- output/ - generated flashcard JSON and CSV files.
- src/
    - state.py - TypedDict state definitions (FlashcardState, CategoryState).
    - models.py - Pydantic models for structured LLM output.
    - nodes/
      - extract_language.py - parses user prompt for language, topic, card count.
      - generate_categories.py - generates relevant categories for topic.
      - generate_flashcards.py - generates flashcards per category (parallel via Send).
      - format_and_save.py - saves output as JSON, CSV, and Anki-import TXT.
    - prompts/
      - extract_language.py - LLM prompt template for language extraction.
      - generate_categories.py - LLM prompt template for category generation.
      - generate_flashcards.py - LLM prompt template for flashcard generation.
