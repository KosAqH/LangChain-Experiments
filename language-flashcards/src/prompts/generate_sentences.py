FLASHCARDS_SENTENCES_PROMPT = """You are a language learning expert creating sentence flashcards for Anki. Generate useful short sentences and phrases for a specific category.

Target language: {language}
Topic: {topic}
Category: {category}

Generate a comprehensive set of sentence/phrase flashcards for this category. For each sentence, provide:
- **category**: The category name
- **type**: Always "sentence"
- **front_en**: The English sentence
- **back_foreign**: The foreign language translation
- **pronunciation_en**: A simple English-approximation pronunciation guide
- **pronunciation_phonetic**: IPA phonetic transcription

Generate as many high-quality sentence flashcards as are useful for this category. Prioritize practical, commonly used phrases and expressions.

Return the result as a structured JSON object with fields:
- "category": the category name
- "flashcards": array of objects with fields: category, type, front_en, back_foreign, pronunciation_en, pronunciation_phonetic"""
