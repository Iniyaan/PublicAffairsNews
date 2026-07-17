"""
==========================================================
Public Affairs Daily Intelligence Portal
Module : News Fetcher
==========================================================
"""

import feedparser
from datetime import datetime, timedelta
from dateutil import parser

from config import (
    get_keywords,
    get_websites,
    NEWS_WINDOW_HOURS
)

# ----------------------------------------------------------
# Google News RSS
# ----------------------------------------------------------

GOOGLE_NEWS_RSS = (
    "https://news.google.com/rss/search?q={query}"
    "&hl=en-IN&gl=IN&ceid=IN:en"
)


# ----------------------------------------------------------
# Build Search Query
# ----------------------------------------------------------

def build_query(keyword, websites):

    site_filter = " OR ".join(
        f"site:{site}" for site in websites
    )

    query = f'{keyword} ({site_filter})'

    return query.replace(" ", "%20")


# ----------------------------------------------------------
# Check Article Date
# ----------------------------------------------------------

def is_recent(published):

    try:

        published_date = parser.parse(published)

        limit = datetime.now(
            published_date.tzinfo
        ) - timedelta(hours=NEWS_WINDOW_HOURS)

        return published_date >= limit

    except Exception:

        return False


# ----------------------------------------------------------
# Fetch News
# ----------------------------------------------------------

def fetch_category(category):

    keywords = get_keywords(category)

    websites = get_websites(category)

    articles = []

    visited = set()

    for keyword in keywords:

        query = build_query(keyword, websites)

        url = GOOGLE_NEWS_RSS.format(query=query)

        feed = feedparser.parse(url)

        for entry in feed.entries:

            if not hasattr(entry, "published"):
                continue

            if not is_recent(entry.published):
                continue

            if entry.link in visited:
                continue

            visited.add(entry.link)

            articles.append({

                "category": category,

                "keyword": keyword,

                "title": entry.title,

                "link": entry.link,

                "published": entry.published,

                "summary": entry.summary
                if hasattr(entry, "summary")
                else "",

                "source": entry.source.title
                if hasattr(entry, "source")
                else "Unknown"

            })

    return articles


# ----------------------------------------------------------
# Fetch All News
# ----------------------------------------------------------

def fetch_all_news():

    news = []

    news.extend(fetch_category("state"))

    news.extend(fetch_category("national"))

    news.extend(fetch_category("global"))

    return news


# ----------------------------------------------------------
# Test
# ----------------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)

    print("Fetching Public Affairs News...")

    print("=" * 60)

    all_news = fetch_all_news()

    print()

    print("Articles Found :", len(all_news))

    print()

    for article in all_news[:10]:

        print("-" * 60)

        print(article["title"])

        print(article["source"])

        print(article["published"])

        print(article["category"])

        print(article["keyword"])

        print(article["link"])

        print()
