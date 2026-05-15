import asyncio
import argparse
import logging
from dotenv import load_dotenv
from db import init_db
from graph import build_graph
from log_config import setup_logging


load_dotenv()
logger = setup_logging()


async def main(query: str):
    await init_db()
    graph = build_graph()

    result = await graph.ainvoke({
        "query": query,
    })

    logger.info("=== NOTE ===")
    logger.info(result["note"])
    logger.info("=== FLASHCARDS ===")
    logger.info(result["flashcards"])
    logger.info("Saved to DB with ID: %s", result.get("note_id"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate notes and Anki flashcards from web sources")
    parser.add_argument("query", help="Query string: topic with optional hints (after - or --) and optional URL")
    args = parser.parse_args()

    asyncio.run(main(args.query))
