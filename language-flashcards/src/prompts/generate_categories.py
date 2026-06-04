CATEGORIES_PROMPT = """You are a language learning expert. Given a target language and topic, generate a comprehensive list of relevant categories for learning vocabulary and phrases.

Target language: {language}
Topic: {topic}

Generate 5-15 categories that cover the most useful and relevant situations, contexts, and themes for this topic. Each category should be concise (2-5 words) and specific enough to generate focused flashcards. If someone mentions trip then take into account the location of the trip but also general categories that would be relevant for any trip. If the topic is more general like "basic" then focus on fundamental categories that are essential for building a strong foundation in the language.

Examples:
- For "basic Italian": Greetings and Introductions, Numbers and Time, In the Restaurant, Shopping, Directions, At the Hotel, Emergencies
- For "trip to mountains in Slovakia": Weather Conditions, Trail Signs, Wildlife, Mountain Huts, Emergency Situations, Directions on Trail, In the Restaurant, Shopping

Return the result as a structured JSON object with a single field "categories" containing an array of strings."""
