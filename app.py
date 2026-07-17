"""
==============================================================
Public Affairs Daily Intelligence Portal
Main Application
Version : 2.0
Author : Iniyaan
==============================================================
"""

import time
import logging

from fetch_news import fetch_all_news
from deduplicate import process_news
from categorizer import categorize_news, sort_articles
from ai_analysis import analyze_news
from website import build_dashboard

# ==========================================================
# LOGGER
# ==========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# ==========================================================
# BANNER
# ==========================================================

def banner():

    logger.info("")

    logger.info("=" * 70)

    logger.info("PUBLIC AFFAIRS DAILY INTELLIGENCE PORTAL")

    logger.info("=" * 70)

    logger.info("")


# ==========================================================
# PIPELINE
# ==========================================================

def run():

    start = time.time()

    banner()

    # ------------------------------------------------------

    logger.info("STEP 1 : Fetching News")

    news = fetch_all_news()

    logger.info("Articles Collected : %s", len(news))

    # ------------------------------------------------------

    logger.info("STEP 2 : Removing Duplicates")

    news = process_news(news)

    logger.info("Remaining Articles : %s", len(news))

    # ------------------------------------------------------

    logger.info("STEP 3 : Categorizing")

    news = categorize_news(news)

    news = sort_articles(news)

    logger.info("Categorization Completed")

    # ------------------------------------------------------

    logger.info("STEP 4 : AI Analysis")

    news = analyze_news(news)

    logger.info("AI Analysis Completed")

    # ------------------------------------------------------

    logger.info("STEP 5 : Generating Website")

    build_dashboard(news)

    logger.info("Website Generated")

    # ------------------------------------------------------

    end = time.time()

    logger.info("")

    logger.info("=" * 70)

    logger.info("PROCESS COMPLETED SUCCESSFULLY")

    logger.info("=" * 70)

    logger.info("")

    logger.info("Execution Time : %.2f Seconds", end - start)

    logger.info("Articles Published : %s", len(news))

    logger.info("")


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    try:

        run()

    except KeyboardInterrupt:

        logger.warning("Program Interrupted.")

    except Exception as error:

        logger.exception(error)
