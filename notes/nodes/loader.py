import requests
from readability import Document
from models import NoteState

def fetch_url_content(url: str) -> str:
    """Fetches the content of the URL and extracts the main article text using readability."""
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

    return content


def loader_node(state: NoteState) -> dict:
    """Fetches and extracts article content from the source URL using readability."""
    if not state["source_urls"]:
        raise ValueError("No source URL available to load")
    
    content_chunks = []
    for url in state["source_urls"]:
        try:
            content_chunks.append(fetch_url_content(url))
        except Exception as e:
            print(f"Error fetching {url}: {e}")
    
    if content_chunks:
        return {"page_content": "\n\n---\n\n".join(content_chunks)}
    else:
        raise ValueError("Failed to fetch content from all provided URLs")
