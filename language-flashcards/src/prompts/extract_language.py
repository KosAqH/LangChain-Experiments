EXTRACT_PROMPT = """You are a language learning assistant. Analyze the user's request and extract structured information.

User request: {user_prompt}

Extract:
1. **language** - The target language to learn (e.g., "Italian", "Slovak", "French")
2. **topic** - The context or theme (e.g., "basic", "trip to mountains", "most important words")
3. **max_cards** - If the user specifies a number (e.g., "100 most important words"), extract that number. Otherwise set to null.

Return the result as a structured JSON object with fields: language, topic, max_cards."""
