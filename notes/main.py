import asyncio
from dotenv import load_dotenv
from db import init_db
from graph import build_graph


load_dotenv()


async def main():
    await init_db()
    graph = build_graph()

    result = await graph.ainvoke({
        "topic": "Python decorators",
        "hints": "Focus on practical examples and common use cases",
        "source_url": None,
    })

    print("=== NOTE ===")
    print(result["note"])
    print("\n=== FLASHCARDS ===")
    print(result["flashcards"])
    print(f"\nSaved to DB with ID: {result.get('note_id')}")


if __name__ == "__main__":
    asyncio.run(main())
