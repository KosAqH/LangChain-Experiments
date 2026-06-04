FLASHCARDS_WORDS_PROMPT = """You are a language learning expert creating vocabulary flashcards for Anki. Generate individual words for a specific category.

Target language: {language}
Topic: {topic}
Category: {category}

Generate a comprehensive set of vocabulary word flashcards for this category. For each word, provide:
- **category**: The category name
- **type**: Always "word"
- **front_en**: The English word
- **back_foreign**: The foreign language translation
- **pronunciation_en**: A simple English-approximation pronunciation guide
- **pronunciation_phonetic**: IPA phonetic transcription
- **example_en**: An example sentence in English showing usage
- **example_foreign**: The example sentence translated to the foreign language

Generate as many high-quality word flashcards as are useful for this category. Prioritize practical, commonly used vocabulary.

Return the result as a structured JSON object with fields:
- "category": the category name
- "flashcards": array of objects with fields: category, type, front_en, back_foreign, pronunciation_en, pronunciation_phonetic, example_en, example_foreign"""
