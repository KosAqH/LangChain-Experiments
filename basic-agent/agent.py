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

# System prompt to steer the agent to be an expert researcher
RESEARCH_INSTRUCTIONS = """You are a Fact-Checker. 
Your goal is to verify the accuracy of the user's input.
- Extract key claims.
- Use `internet_search` to find supporting or contradicting evidence from reputable sources. Verify the credibility of sources.
- Value scientific consensus and expert opinions more than individual claims and political statements.
- Summarize the evidence for each claim, noting any contradictions or uncertainties.
- Assign a 'Confidence Score' (0-100) to each claim.

You must present your findings in markdown format as follows:
Claim: <claim>
Evidence: <summary of evidence>
References: <list of sources>
Decision: <True/False/Uncertain>
Confidence Score: <score>
---
"""

if __name__ == "__main__":
    model = ChatOpenRouter(model="openai/gpt-4o-mini", max_tokens=16000)

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
