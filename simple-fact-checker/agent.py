from urllib import response

import dotenv
import json
import os
import time
from pathlib import Path
from typing import Literal

from deepagents import create_deep_agent
from langchain_openrouter import ChatOpenRouter
from tavily import TavilyClient

dotenv.load_dotenv()
tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent

def sanitize_filename(name: str) -> str:
    RESTRICTED_CHARS = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in RESTRICTED_CHARS:
        name = name.replace(char, '')
    return name

def save_markdown(content: str, query: str) -> None:
    safe_query = sanitize_filename(query[:20].replace(' ', '_'))
    filename = SCRIPT_DIR / "reports" / f"{int(time.time())}_{safe_query}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Report saved to {filename}")

def log_search(query: str, data: dict) -> None:
    safe_query = sanitize_filename(query[:20].replace(' ', '_'))
    filename = SCRIPT_DIR / "logs" / "raw_searches" / f"{int(time.time())}_{safe_query}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
) -> list[dict]:
    """Run a web search"""
    tavily_response = tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )
    log_search(query, tavily_response)
    return tavily_response["results"]

RESEARCH_INSTRUCTIONS = """You are a professionalFact-Checker. 
Your goal is to verify the accuracy of the user's input.

1. **Deconstruct**: Break user input into individual testable claims.
2. **Verify**: Use `internet_search` for each claim. Prioritize peer-reviewed research, official government data, and primary news sources.
3. **Cross-Reference**: Explicitly look for counter-arguments or conflicting data.
4. **Evaluate**: Use the 'CRAAP' test (Currency, Relevance, Authority, Accuracy, Purpose).

You must present your findings in markdown format as follows:
## Claim
<claim>
## Evidence:
<summary of evidence>
## References:
<list of sources>
## Decision: 
<True/False/Uncertain>
## Confidence Score:
<score>
"""

if __name__ == "__main__":
    (SCRIPT_DIR / "logs" / "raw_searches").mkdir(parents=True, exist_ok=True)
    (SCRIPT_DIR / "reports").mkdir(parents=True, exist_ok=True)

    model = ChatOpenRouter(model="openai/gpt-4o-mini", max_tokens=16000, temperature=0)

    agent = create_deep_agent(
        model=model,
        tools=[internet_search],
        system_prompt=RESEARCH_INSTRUCTIONS,
    )

    while True:
        user_input = input("Enter a query (or 'quit' to exit): ")
        if user_input.lower() == "quit":
            break
        
        result = agent.invoke({"messages": [{"role": "user", "content": user_input}]})

        final_content = result["messages"][-1].content
        print(f"{final_content}")
        save_markdown(final_content, user_input)
