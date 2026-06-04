from typing import cast
from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter
from src.models import ExtractedPrompt
from src.prompts.extract_language import EXTRACT_PROMPT
from src.state import FlashcardState


load_dotenv()

model = ChatOpenRouter(
    model="openai/gpt-4o-mini",
    temperature=0,
)


def extract_language(state: FlashcardState) -> dict:
    user_prompt = state["user_prompt"]
    prompt = EXTRACT_PROMPT.format(user_prompt=user_prompt)
    response = cast(ExtractedPrompt, model.with_structured_output(ExtractedPrompt).invoke(prompt))
    return {
        "target_language": response.language,
        "topic_context": response.topic,
        "max_cards": response.max_cards,
    }
