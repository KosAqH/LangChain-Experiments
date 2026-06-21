import logging

from src.state import FlashcardState


logger = logging.getLogger(__name__)


def _show_categories(categories: list[str]) -> None:
    print("\n=== Generated categories ===")
    for i, cat in enumerate(categories, 1):
        print(f"  {i}. {cat}")
    print()


def human_review_categories(state: FlashcardState) -> dict:
    categories = list(state["categories"])

    if not categories:
        logger.info("No categories to review, skipping")
        return {"categories": categories}

    logger.info("Human review: waiting for user input on categories")
    _show_categories(categories)

    while True:
        print("Options: a <name> (add), r <num> (remove), l (list), d (done)")
        user_input = input("What would you like to do? ").strip()

        if not user_input:
            continue

        parts = user_input.split(maxsplit=1)
        command = parts[0].lower()

        if command == "d":
            break

        elif command == "l":
            _show_categories(categories)

        elif command == "a":
            if len(parts) < 2:
                print("Usage: a <category name>")
                continue
            new_name = parts[1].strip().rstrip(",")
            if new_name:
                categories.append(new_name)
                print(f"  Added: {new_name}")

        elif command == "r":
            if len(parts) < 2:
                print("Usage: r <number>")
                continue
            try:
                idx = int(parts[1]) - 1
                if idx < 0 or idx >= len(categories):
                    print(f"  Invalid number. Choose 1–{len(categories)}")
                    continue
                removed = categories.pop(idx)
                print(f"  Removed: {removed}")
            except ValueError:
                print("  Please enter a valid number")

        else:
            print("  Unknown command. Options: a <name>, r <num>, l, d")

    logger.info("Human review finished. Final categories: %s", categories)
    return {"categories": categories}
