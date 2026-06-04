import json
import csv
import os
import re
import logging
from datetime import datetime
from src.state import FlashcardState


logger = logging.getLogger(__name__)


def _sanitize_filename(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    text = re.sub(r"[-\s]+", "-", text)
    return text[:50]


def format_and_save(state: FlashcardState) -> dict:
    flashcards = state["flashcards"]
    lang = state["target_language"]
    topic = state["topic_context"]

    base = _sanitize_filename(f"{lang}-{topic}")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join("output", f"{base}_{timestamp}")
    os.makedirs(output_dir, exist_ok=True)
    logger.info("Saving %d flashcards to %s", len(flashcards), output_dir)

    json_path = os.path.join(output_dir, "flashcards.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(flashcards, f, ensure_ascii=False, indent=2)
    logger.info("Saved JSON: %s", json_path)

    csv_path = os.path.join(output_dir, "flashcards.csv")
    fieldnames = [
        "front_en",
        "back_foreign",
        "pronunciation_en",
        "pronunciation_phonetic",
        "example_en",
        "example_foreign",
        "category",
        "type",
    ]
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for card in flashcards:
            writer.writerow({k: card.get(k, "") for k in fieldnames})
    logger.info("Saved CSV: %s", csv_path)

    anki_path = os.path.join(output_dir, "anki_import.txt")
    with open(anki_path, "w", encoding="utf-8", newline="") as f:
        for card in flashcards:
            row = "\t".join(
                [
                    card.get("front_en", ""),
                    card.get("back_foreign", ""),
                    card.get("pronunciation_en", ""),
                    card.get("pronunciation_phonetic", ""),
                    card.get("example_en", ""),
                    card.get("example_foreign", ""),
                    card.get("category", ""),
                ]
            )
            f.write(row + "\n")
    logger.info("Saved Anki import: %s", anki_path)

    return {"output_file": output_dir}
