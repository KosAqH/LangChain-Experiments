import aiosqlite
import json
from datetime import datetime


DB_PATH = "notes.db"


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                resources TEXT,
                note TEXT,
                flashcards TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()


async def save_note(topic: str, resources: list[str], note: str, flashcards: str) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            """
            INSERT INTO notes (topic, resources, note, flashcards)
            VALUES (?, ?, ?, ?)
            """,
            (topic, json.dumps(resources), note, flashcards),
        )
        await db.commit()
        return cursor.lastrowid
