import requests
from readability import Document
from models import NoteState


def loader_node(state: NoteState) -> dict:
    """Fetches and extracts article content from the source URL using readability."""
    url = state["source_url"]
    if not url:
        raise ValueError("No source URL available to load")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    doc = Document(response.text)
    html_content = doc.summary()

    # Strip HTML tags to get plain text
    from lxml.html import fromstring
    tree = fromstring(html_content)
    text = tree.text_content()

    # Clean up excessive whitespace
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    content = "\n".join(lines)

    return {"page_content": content}
