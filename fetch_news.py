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
