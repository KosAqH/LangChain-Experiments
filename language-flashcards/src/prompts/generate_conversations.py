FLASHCARDS_CONVERSATIONS_PROMPT = """You are a language learning expert creating conversation flashcards for Anki. Generate short back-and-forth dialogues (2-4 lines) for a specific category.

Target language: {language}
Topic: {topic}
Category: {category}

{limit_instruction}

For each conversation, provide:
- **category**: The category name
- **front_en**: The English dialogue
- **back_foreign**: The foreign language translation
- **pronunciation_en**: A simple English-approximation pronunciation guide
- **pronunciation_phonetic**: IPA phonetic transcription

Each conversation should be a short back-and-forth exchange (2-4 lines). Prioritize practical, real-world dialogue scenarios.

Return the result as a structured JSON object with fields:
- "category": the category name
- "flashcards": array of objects with fields: category, front_en, back_foreign, pronunciation_en, pronunciation_phonetic"""
