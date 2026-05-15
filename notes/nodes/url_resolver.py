import os
from tavily import TavilyClient
from models import NoteState


def url_resolver_node(state: NoteState) -> dict:
    """Uses Tavily to find a source URL if one wasn't provided."""
    if state.get("source_url"):
        return {"source_url": state["source_url"], "source_urls": state.get("source_urls", [])}

    client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
    search_query = f"{state['topic']} {' '.join(state['hints'].split()[:5])}".strip()

    results = client.search(
        query=search_query,
        max_results=3,
        search_depth="advanced",
    )

    urls = []
    for result in results.get("results", []):
        url = result.get("url")
        if url:
            urls.append(url)

    if not urls:
        raise ValueError(f"Tavily search returned no results for: {search_query}")

    return {"source_url": urls[0], "source_urls": urls}
