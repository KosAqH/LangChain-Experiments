FLASHCARDS_CONVERSATIONS_PROMPT = """You are a language learning expert creating conversation flashcards for Anki. Generate short back-and-forth dialogues (2-4 lines) for a specific category.

Target language: {language}
Topic: {topic}
Category: {category}

Generate a comprehensive set of conversation flashcards for this category. Each conversation should be a short back-and-forth exchange (2-4 lines). For each conversation, provide:
- **category**: The category name
- **type**: Always "conversation"
- **front_en**: The English dialogue
- **back_foreign**: The foreign language translation
- **pronunciation_en**: A simple English-approximation pronunciation guide
- **pronunciation_phonetic**: IPA phonetic transcription

Generate as many high-quality conversation flashcards as are useful for this category. Prioritize practical, real-world dialogue scenarios.

Return the result as a structured JSON object with fields:
- "category": the category name
- "flashcards": array of objects with fields: category, type, front_en, back_foreign, pronunciation_en, pronunciation_phonetic"""
