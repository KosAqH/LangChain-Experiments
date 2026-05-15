import requests
from bs4 import BeautifulSoup
from models import NoteState


def loader_node(state: NoteState) -> dict:
    """Fetches and extracts text content from the source URL."""
    url = state["source_url"]
    if not url:
        raise ValueError("No source URL available to load")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove script, style, nav, footer, header elements
    for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
        element.decompose()

    # Extract text from main content or body
    main = soup.find("main") or soup.find("article") or soup.find("body")
    text = main.get_text(separator="\n", strip=True) if main else soup.get_text(separator="\n", strip=True)

    # Clean up excessive whitespace
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    content = "\n".join(lines)

    return {"page_content": content}
