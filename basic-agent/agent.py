import os
import dotenv

from typing import Literal
from tavily import TavilyClient
from deepagents import create_deep_agent
from langchain_openrouter import ChatOpenRouter

dotenv.load_dotenv()


tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """Run a web search"""
    print(f"Running internet search for query: {query}")
    return tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )

RESEARCH_INSTRUCTIONS = """You are a professionalFact-Checker. 
Your goal is to verify the accuracy of the user's input.

1. **Deconstruct**: Break user input into individual testable claims.
2. **Verify**: Use `internet_search` for each claim. Prioritize peer-reviewed research, official government data, and primary news sources.
3. **Cross-Reference**: Explicitly look for counter-arguments or conflicting data.
4. **Evaluate**: Use the 'CRAAP' test (Currency, Relevance, Authority, Accuracy, Purpose).

You must present your findings in markdown format as follows:
Claim: <claim>
Evidence: <summary of evidence>
References: <list of sources>
Decision: <True/False/Uncertain>
Confidence Score: <score>
"""

if __name__ == "__main__":
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

        print(result["messages"][-1].content)
