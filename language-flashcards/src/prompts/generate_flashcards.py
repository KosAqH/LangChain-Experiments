FLASHCARDS_PROMPT = """You are a language learning expert creating flashcards for Anki. Generate vocabulary and phrases for a specific category.

Target language: {language}
Topic: {topic}
Category: {category}

Generate a comprehensive set of flashcards for this category. Include:

1. **Individual words** - Key vocabulary items
2. **Short sentences** - Useful phrases
3. **Conversations** - Short back-and-forth exchanges (2-4 lines)

For each flashcard, provide:
- **category**: The category name
- **type**: Either "word", "sentence", or "conversation"
- **front_en**: The English text (this goes on the front of the Anki card)
- **back_foreign**: The foreign language translation (this goes on the back)
- **pronunciation_en**: A simple English-approximation pronunciation guide
- **pronunciation_phonetic**: IPA phonetic transcription
- **example_en**: For words only, an example sentence in English showing usage
- **example_foreign**: For words only, the example sentence translated to the foreign language

Generate as many high-quality flashcards as are useful for this category. Prioritize practical, commonly used vocabulary and phrases.

Return the result as a structured JSON object with fields:
- "category": the category name
- "flashcards": array of objects with fields: category, type, front_en, back_foreign, pronunciation_en, pronunciation_phonetic, example_en, example_foreign"""
