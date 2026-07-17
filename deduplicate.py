"""
==========================================================
Public Affairs Daily Intelligence Portal
Module : Duplicate News Removal
==========================================================
"""

import json
from pathlib import Path
from difflib import SequenceMatcher

from config import HISTORY


# ==========================================================
# History File
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

HISTORY_FILE = BASE_DIR / "data" / "history.json"


# ==========================================================
# Similarity Checker
# ==========================================================

def similarity(text1, text2):
    """
    Compare two headlines.
    Returns similarity between 0 and 1.
    """

    return SequenceMatcher(
        None,
        text1.lower(),
        text2.lower()
    ).ratio()


# ==========================================================
# Already Published?
# ==========================================================

def already_published(title):

    for article in HISTORY:

        if similarity(title, article["title"]) > 0.90:
            return True

    return False


# ==========================================================
# Remove Duplicates
# ==========================================================

def remove_duplicates(news):

    unique = []

    seen_links = set()

    seen_titles = []

    for article in news:

        # Duplicate URL
        if article["link"] in seen_links:
            continue

        seen_links.add(article["link"])

        duplicate = False

        # Similar headline
        for title in seen_titles:

            if similarity(
                article["title"],
                title
            ) > 0.90:

                duplicate = True
                break

        if duplicate:
            continue

        # Previous day's report
        if already_published(article["title"]):
            continue

        seen_titles.append(article["title"])

        unique.append(article)

    return unique


# ==========================================================
# Save History
# ==========================================================

def save_history(news):

    history = HISTORY.copy()

    for article in news:

        history.append({

            "title": article["title"],

            "source": article["source"],

            "published": article["published"]

        })

    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            history,
            file,
            indent=4,
            ensure_ascii=False
        )


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    print("Duplicate Module Ready")
