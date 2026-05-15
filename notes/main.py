import asyncio
import argparse
from dotenv import load_dotenv
from db import init_db
from graph import build_graph


load_dotenv()


async def main(query: str):
    await init_db()
    graph = build_graph()

    result = await graph.ainvoke({
        "query": query,
    })

    print("=== NOTE ===")
    print(result["note"])
    print("\n=== FLASHCARDS ===")
    print(result["flashcards"])
    print(f"\nSaved to DB with ID: {result.get('note_id')}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate notes and Anki flashcards from web sources")
    parser.add_argument("query", help="Query string: topic with optional hints (after - or --) and optional URL")
    args = parser.parse_args()

    asyncio.run(main(args.query))
