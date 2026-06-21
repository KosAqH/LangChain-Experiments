PLAN_DISTRIBUTION_PROMPT = """You are a language learning expert planning flashcard distribution. Given a target language, topic, list of categories, and a total card limit, distribute the cards intelligently across categories and card types (word, sentence, conversation).

Target language: {language}
Topic: {topic}
Total card limit: {max_cards}
Categories: {categories}

Distribute the {max_cards} cards across the categories and three card types (word, sentence, conversation). Consider:
- Some categories need more vocabulary (word cards) — e.g., "In the Restaurant" needs many words
- Some categories need more phrases (sentence cards) — e.g., "Emergencies" needs key phrases
- Some categories benefit from dialogues (conversation cards) — e.g., "Shopping" needs back-and-forth practice
- Prioritize practical, high-value content
- Each category should get at least 1 card of each type if possible
- The sum of all limits must equal exactly {max_cards}

Return the result as a structured JSON object with a single field "distribution" containing an array of objects, each with fields: category, type (one of "word", "sentence", "conversation"), limit (integer).
Example:
{{
  "distribution": [
    {{"category": "Greetings", "type": "word", "limit": 5}},
    {{"category": "Greetings", "type": "sentence", "limit": 3}},
    {{"category": "Greetings", "type": "conversation", "limit": 2}},
    {{"category": "In the Restaurant", "type": "word", "limit": 8}},
    ...
  ]
}}"""
