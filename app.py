from website import generate_website
"""
===========================================================
Public Affairs Daily Intelligence Portal
Main Application
Version : 1.0
===========================================================
"""

from utils import log

from fetch_news import fetch_all_news

from deduplicate import (
    remove_duplicates,
    save_history
)

from categorizer import categorize_news

from ai_analysis import analyze_news


def main():

    log("==============================================")

    log("Public Affairs Daily Intelligence Portal")

    log("==============================================")

    # ------------------------------------------

    log("Fetching News...")

    news = fetch_all_news()

    log(f"Articles Collected : {len(news)}")

    # ------------------------------------------

    log("Removing Duplicate News...")

    news = remove_duplicates(news)

    log(f"Unique Articles : {len(news)}")

    # ------------------------------------------

    log("Categorizing News...")

    news = categorize_news(news)

    # ------------------------------------------

    log("Generating AI Analysis...")

    news = analyze_news(news)

    # ------------------------------------------

    log("Saving History...")

    save_history(news)

    # ------------------------------------------

    log("Generating Website...")
generate_website(news)
    # ------------------------------------------

    log("Completed Successfully.")

    return news


if __name__ == "__main__":

    main()
