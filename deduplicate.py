"""
==============================================================
Public Affairs Daily Intelligence Portal
Module : Duplicate Detection Engine
Version : 2.0
Author : Iniyaan
==============================================================
"""

import json
import logging
from pathlib import Path
from difflib import SequenceMatcher

from utils import clean_text

# ==========================================================
# LOGGER
# ==========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

HISTORY_FILE = DATA_DIR / "history.json"

# ==========================================================
# SOURCE PRIORITY
# Lower number = Higher Priority
# ==========================================================

SOURCE_PRIORITY = {

    "Reuters": 1,

    "The Hindu": 2,

    "Times of India": 3,

    "NDTV": 4,

    "India Today": 5,

    "News18": 6,

    "Daily Thanthi": 7,

    "Dinamalar": 8,

    "Thanthi TV": 9,

    "Puthiya Thalaimurai": 10,

    "Unknown": 99

}

# ==========================================================
# HISTORY
# ==========================================================

def load_history():

    """
    Load previous articles.
    """

    if not HISTORY_FILE.exists():

        return []

    try:

        with open(

            HISTORY_FILE,

            "r",

            encoding="utf-8"

        ) as file:

            return json.load(file)

    except Exception as error:

        logger.warning(

            "Unable to load history : %s",

            error

        )

        return []


# ==========================================================
# SAVE HISTORY
# ==========================================================

def save_history(history):

    """
    Save history.
    """

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
# TITLE SIMILARITY
# ==========================================================

def similarity(title1, title2):

    """
    Compare two headlines.

    Returns value between

    0 and 1
    """

    return SequenceMatcher(

        None,

        clean_text(title1),

        clean_text(title2)

    ).ratio()


# ==========================================================
# SAME ARTICLE?
# ==========================================================

def same_article(article1, article2):

    """
    Decide whether two articles
    are likely describing the
    same event.
    """

    # Same URL

    if article1["link"] == article2["link"]:

        return True

    # Very similar headline

    score = similarity(

        article1["title"],

        article2["title"]

    )

    if score >= 0.90:

        return True

    return False


# ==========================================================
# SOURCE RANK
# ==========================================================

def source_rank(source):

    return SOURCE_PRIORITY.get(

        source,

        99

    )


# ==========================================================
# KEEP BETTER ARTICLE
# ==========================================================

def better_article(article1, article2):

    """
    Keep the article from the
    higher priority source.

    If same source,
    keep higher score.
    """

    rank1 = source_rank(

        article1["source"]

    )

    rank2 = source_rank(

        article2["source"]

    )

    if rank1 < rank2:

        return article1

    if rank2 < rank1:

        return article2

    if article1["score"] >= article2["score"]:

        return article1

    return article2
    # ==========================================================
# HISTORY CHECK
# ==========================================================

def already_in_history(article, history):

    """
    Check whether the article
    already exists in history.
    """

    for old_article in history:

        try:

            if article["link"] == old_article.get("link", ""):
                return True

            score = similarity(

                article["title"],

                old_article.get("title", "")

            )

            if score >= 0.90:
                return True

        except Exception:
            continue

    return False


# ==========================================================
# UPDATED ARTICLE
# ==========================================================

def is_updated(article, history):

    """
    Check if an article is an
    updated version of an
    existing story.
    """

    for old_article in history:

        score = similarity(

            article["title"],

            old_article.get("title", "")

        )

        if 0.75 <= score < 0.90:

            return True

    return False


# ==========================================================
# REMOVE DUPLICATES
# ==========================================================

def remove_duplicates(news):

    """
    Remove duplicate articles.

    Returns

    Unique News
    """

    logger.info("Removing duplicate articles...")

    unique_news = []

    for article in news:

        duplicate_found = False

        for index, existing in enumerate(unique_news):

            if same_article(article, existing):

                better = better_article(

                    article,

                    existing

                )

                unique_news[index] = better

                duplicate_found = True

                break

        if not duplicate_found:

            unique_news.append(article)

    logger.info(

        "Unique Articles : %s",

        len(unique_news)

    )

    return unique_news


# ==========================================================
# REMOVE OLD ARTICLES
# ==========================================================

def remove_history(news):

    """
    Remove articles already
    published previously.
    """

    history = load_history()

    filtered = []

    skipped = 0

    updated = 0

    for article in news:

        if already_in_history(

            article,

            history

        ):

            skipped += 1
            continue

        if is_updated(

            article,

            history

        ):

            article["updated"] = True

            updated += 1

        else:

            article["updated"] = False

        filtered.append(article)

    logger.info(

        "Skipped History : %s",

        skipped

    )

    logger.info(

        "Updated Stories : %s",

        updated

    )

    logger.info(

        "Remaining News : %s",

        len(filtered)

    )

    return filtered
    # ==========================================================
# UPDATE HISTORY
# ==========================================================

def update_history(news):

    """
    Add today's unique news
    into history.json
    """

    history = load_history()

    for article in news:

        history.append({

            "title": article["title"],

            "link": article["link"],

            "source": article["source"],

            "published": article["published"]

        })

    # Keep latest 5000 records

    if len(history) > 5000:

        history = history[-5000:]

    save_history(history)

    logger.info(

        "History Updated : %s",

        len(history)

    )


# ==========================================================
# STATISTICS
# ==========================================================

def statistics(original_news, final_news):

    duplicates_removed = (

        len(original_news)

        - len(final_news)

    )

    stats = {

        "original": len(original_news),

        "final": len(final_news),

        "duplicates_removed": duplicates_removed

    }

    logger.info("")

    logger.info("=" * 50)

    logger.info("Duplicate Detection Statistics")

    logger.info("=" * 50)

    logger.info(

        "Original Articles      : %s",

        stats["original"]

    )

    logger.info(

        "Duplicate Removed      : %s",

        stats["duplicates_removed"]

    )

    logger.info(

        "Remaining Articles     : %s",

        stats["final"]

    )

    logger.info("=" * 50)

    logger.info("")

    return stats


# ==========================================================
# PROCESS NEWS
# ==========================================================

def process_news(news):

    """
    Complete duplicate engine

    Steps

    1 Remove duplicate URLs

    2 Remove similar headlines

    3 Remove already published

    4 Mark updated stories

    5 Update history

    """

    logger.info("")

    logger.info(

        "Processing News..."

    )

    original_news = news.copy()

    news = remove_duplicates(

        news

    )

    news = remove_history(

        news

    )

    update_history(

        news

    )

    statistics(

        original_news,

        news

    )

    return news
    # ==========================================================
# EXPORT CLEANED NEWS
# ==========================================================

def export_clean_news(news, filename="clean_news.json"):
    """
    Export cleaned news for debugging/testing.
    """

    try:

        with open(

            filename,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                news,

                file,

                indent=4,

                ensure_ascii=False

            )

        logger.info(

            "Clean news exported : %s",

            filename

        )

    except Exception as error:

        logger.error(

            "Export failed : %s",

            error

        )


# ==========================================================
# SEARCH ARTICLE
# ==========================================================

def search(news, keyword):

    keyword = keyword.lower()

    results = []

    for article in news:

        if (

            keyword in article["title"].lower()

            or

            keyword in article.get(

                "summary",

                ""

            ).lower()

        ):

            results.append(article)

    return results


# ==========================================================
# PRINT SAMPLE
# ==========================================================

def print_sample(news, limit=10):

    logger.info("")

    logger.info("=" * 60)

    logger.info("Sample Clean Articles")

    logger.info("=" * 60)

    for index, article in enumerate(news[:limit], start=1):

        logger.info(

            "%s. %s",

            index,

            article["title"]

        )

        logger.info(

            "Source : %s",

            article["source"]

        )

        logger.info(

            "Category : %s",

            article["category"]

        )

        logger.info(

            "Score : %s",

            article["score"]

        )

        logger.info(

            "Updated : %s",

            article.get(

                "updated",

                False

            )

        )

        logger.info("-" * 60)


# ==========================================================
# MAIN TEST
# ==========================================================

if __name__ == "__main__":

    from fetch_news import fetch_all_news

    logger.info("")

    logger.info("=" * 60)

    logger.info("Duplicate Detection Engine")

    logger.info("=" * 60)

    try:

        news = fetch_all_news()

        logger.info(

            "Fetched Articles : %s",

            len(news)

        )

        clean_news = process_news(news)

        export_clean_news(clean_news)

        print_sample(clean_news)

        logger.info("")

        logger.info(

            "Duplicate Detection Completed Successfully."

        )

    except Exception as error:

        logger.exception(

            "Duplicate Engine Failed : %s",

            error

        )
    
