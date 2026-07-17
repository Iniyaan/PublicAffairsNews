"""
==============================================================
Public Affairs Daily Intelligence Portal
Module : Fetch News
Version : 2.0
Author : Iniyaan
==============================================================
"""

import time
import logging
import urllib.parse
from datetime import datetime, timedelta, timezone

import feedparser
import requests
from dateutil import parser

from config import (
    NEWS_WINDOW_HOURS,
    get_keywords,
    get_websites
)

# ==========================================================
# LOGGER
# ==========================================================

logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(message)s"

)

logger = logging.getLogger(__name__)

# ==========================================================
# CONSTANTS
# ==========================================================

GOOGLE_NEWS_RSS = (

    "https://news.google.com/rss/search"

)

HEADERS = {

    "User-Agent":

    "Mozilla/5.0 PublicAffairsNewsBot/2.0"

}

REQUEST_TIMEOUT = 30

MAX_RETRY = 3

SLEEP_TIME = 2

# ==========================================================
# GOOGLE QUERY
# ==========================================================

def build_query(keyword, websites):

    """
    Build Google News query

    Example

    SIPCOT
    site:thehindu.com
    OR
    site:timesofindia.com
    """

    site_query = " OR ".join(

        f"site:{site}"

        for site in websites

    )

    query = (

        f'"{keyword}" '

        f'({site_query}) '

        "when:2d"

    )

    return query

# ==========================================================
# RSS URL
# ==========================================================

def rss_url(query):

    encoded = urllib.parse.quote(query)

    return (

        f"{GOOGLE_NEWS_RSS}"

        f"?q={encoded}"

        "&hl=en-IN"

        "&gl=IN"

        "&ceid=IN:en"

    )

# ==========================================================
# HTTP REQUEST
# ==========================================================

def get_feed(url):

    """
    Download RSS safely
    """

    for attempt in range(MAX_RETRY):

        try:

            response = requests.get(

                url,

                headers=HEADERS,

                timeout=REQUEST_TIMEOUT

            )

            response.raise_for_status()

            return feedparser.parse(

                response.content

            )

        except Exception as error:

            logger.warning(

                "Attempt %s failed : %s",

                attempt + 1,

                error

            )

            time.sleep(SLEEP_TIME)

    logger.error(

        "Unable to download RSS Feed."

    )

    return None

# ==========================================================
# DATE FILTER
# ==========================================================

def within_window(date_string):

    """
    Return True

    if article is

    within NEWS_WINDOW_HOURS
    """

    try:

        published = parser.parse(date_string)

        if published.tzinfo is None:

            published = published.replace(

                tzinfo=timezone.utc

            )

        now = datetime.now(

            timezone.utc

        )

        cutoff = now - timedelta(

            hours=NEWS_WINDOW_HOURS

        )

        return published >= cutoff

    except Exception:

        return False

# ==========================================================
# CLEAN TITLE
# ==========================================================

def clean_title(title):

    return (

        title

        .replace("\n", " ")

        .replace("\r", " ")

        .strip()

    )

# ==========================================================
# SCORE ARTICLE
# ==========================================================

def score_article(article):

    score = 0

    title = article["title"].lower()

    summary = article["summary"].lower()

    important = [

        "government",

        "policy",

        "cabinet",

        "budget",

        "investment",

        "manufacturing",

        "industry",

        "employment",

        "labour",

        "infrastructure",

        "finance",

        "trade",

        "export",

        "import",

        "power"

    ]

    for word in important:

        if word in title:

            score += 5

        if word in summary:

            score += 2

    return score
# ==========================================================
# EXTRACT ARTICLE
# ==========================================================

def extract_article(entry, category, keyword):

    """
    Convert RSS entry to dictionary
    """

    try:

        title = clean_title(entry.title)

        link = getattr(entry, "link", "").strip()

        summary = getattr(entry, "summary", "").strip()

        published = getattr(entry, "published", "")

        source = "Unknown"

        if hasattr(entry, "source"):

            source = getattr(entry.source, "title", "Unknown")

        if not title or not link:
            return None

        if not within_window(published):
            return None

        article = {

            "title": title,

            "summary": summary,

            "link": link,

            "published": published,

            "source": source,

            "keyword": keyword,

            "category": category,

            "score": 0

        }

        article["score"] = score_article(article)

        return article

    except Exception as error:

        logger.warning(

            "Unable to process article : %s",

            error

        )

        return None


# ==========================================================
# FETCH ONE KEYWORD
# ==========================================================

def fetch_keyword(category, keyword):

    """
    Fetch articles for one keyword
    """

    logger.info(

        "Searching : %s",

        keyword

    )

    websites = get_websites(category)

    query = build_query(

        keyword,

        websites

    )

    url = rss_url(query)

    feed = get_feed(url)

    if feed is None:

        return []

    articles = []

    for entry in feed.entries:

        article = extract_article(

            entry,

            category,

            keyword

        )

        if article:

            articles.append(article)

    logger.info(

        "%s Articles Found",

        len(articles)

    )

    return articles


# ==========================================================
# FETCH CATEGORY
# ==========================================================

def fetch_category(category):

    """
    Fetch all keywords
    for one category
    """

    logger.info(

        "Category : %s",

        category

    )

    keywords = get_keywords(category)

    all_articles = []

    for keyword in keywords:

        try:

            articles = fetch_keyword(

                category,

                keyword

            )

            all_articles.extend(

                articles

            )

        except Exception as error:

            logger.warning(

                "%s",

                error

            )

    logger.info(

        "%s Total Articles",

        len(all_articles)

    )

    return all_articles


# ==========================================================
# REMOVE DUPLICATE URL
# ==========================================================

def remove_duplicate_urls(news):

    unique = []

    visited = set()

    for article in news:

        url = article["link"]

        if url in visited:

            continue

        visited.add(url)

        unique.append(article)

    logger.info(

        "Unique URL : %s",

        len(unique)

    )

    return unique
    # ==========================================================
# SORT NEWS
# ==========================================================

def sort_news(news):

    """
    Sort news by

    1. Score (Highest)

    2. Published Date (Latest)
    """

    try:

        return sorted(

            news,

            key=lambda article: (

                article["score"],

                parser.parse(article["published"])

            ),

            reverse=True

        )

    except Exception:

        return news


# ==========================================================
# REMOVE EMPTY ARTICLES
# ==========================================================

def remove_empty(news):

    cleaned = []

    for article in news:

        if not article["title"]:

            continue

        if not article["link"]:

            continue

        cleaned.append(article)

    logger.info(

        "Valid Articles : %s",

        len(cleaned)

    )

    return cleaned


# ==========================================================
# FETCH ALL NEWS
# ==========================================================

def fetch_all_news():

    logger.info(

        "====================================="

    )

    logger.info(

        "Fetching Public Affairs News"

    )

    logger.info(

        "====================================="

    )

    news = []

    # --------------------------------------

    state_news = fetch_category(

        "state"

    )

    news.extend(

        state_news

    )

    # --------------------------------------

    national_news = fetch_category(

        "national"

    )

    news.extend(

        national_news

    )

    # --------------------------------------

    global_news = fetch_category(

        "global"

    )

    news.extend(

        global_news

    )

    logger.info(

        "Collected Articles : %s",

        len(news)

    )

    # --------------------------------------

    news = remove_empty(

        news

    )

    news = remove_duplicate_urls(

        news

    )

    news = sort_news(

        news

    )

    logger.info(

        "Final Articles : %s",

        len(news)

    )

    return news


# ==========================================================
# ARTICLE STATISTICS
# ==========================================================

def news_statistics(news):

    stats = {

        "total": len(news),

        "state": 0,

        "national": 0,

        "global": 0

    }

    for article in news:

        category = article["category"]

        if category in stats:

            stats[category] += 1

    return stats


# ==========================================================
# DISPLAY SUMMARY
# ==========================================================

def print_statistics(news):

    stats = news_statistics(news)

    logger.info("")

    logger.info("========== NEWS SUMMARY ==========")

    logger.info(

        "State Articles     : %s",

        stats["state"]

    )

    logger.info(

        "National Articles  : %s",

        stats["national"]

    )

    logger.info(

        "Global Articles    : %s",

        stats["global"]

    )

    logger.info(

        "Total Articles     : %s",

        stats["total"]

    )

    logger.info(

        "=================================="

    )
    # ==========================================================
# EXPORT NEWS
# ==========================================================

def export_news(news, filename="latest_news.json"):
    """
    Export collected news to JSON.
    """

    import json

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

        "News exported : %s",

        filename

    )


# ==========================================================
# SEARCH NEWS
# ==========================================================

def search_news(news, keyword):

    keyword = keyword.lower()

    results = []

    for article in news:

        if (

            keyword in article["title"].lower()

            or

            keyword in article["summary"].lower()

        ):

            results.append(article)

    return results


# ==========================================================
# MAIN TEST
# ==========================================================

if __name__ == "__main__":

    logger.info("")

    logger.info("=" * 60)

    logger.info("Public Affairs News Engine")

    logger.info("=" * 60)

    try:

        news = fetch_all_news()

        print_statistics(news)

        export_news(news)

        logger.info("")

        logger.info("Top 10 Articles")

        logger.info("-" * 60)

        for index, article in enumerate(news[:10], start=1):

            logger.info(

                "%s. %s",

                index,

                article["title"]

            )

            logger.info(

                "Source    : %s",

                article["source"]

            )

            logger.info(

                "Published : %s",

                article["published"]

            )

            logger.info(

                "Category  : %s",

                article["category"]

            )

            logger.info(

                "Score     : %s",

                article["score"]

            )

            logger.info(

                "URL       : %s",

                article["link"]

            )

            logger.info("-" * 60)

    except Exception as error:

        logger.exception(

            "News Engine Failed : %s",

            error

        )
