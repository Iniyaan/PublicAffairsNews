"""
==============================================================
Public Affairs Daily Intelligence Portal
Module : News Categorizer
Version : 2.0
Author : Iniyaan
==============================================================
"""

import logging
from pathlib import Path

from utils import read_json, clean_text

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

CATEGORY_FILE = DATA_DIR / "category_mapping.json"

DEPARTMENT_FILE = DATA_DIR / "department_mapping.json"

# ==========================================================
# LOAD MAPPING FILES
# ==========================================================

CATEGORY_MAPPING = read_json("category_mapping.json")

DEPARTMENT_MAPPING = read_json("department_mapping.json")

if CATEGORY_MAPPING is None:
    CATEGORY_MAPPING = {}

if DEPARTMENT_MAPPING is None:
    DEPARTMENT_MAPPING = {}

# ==========================================================
# PRIORITY KEYWORDS
# ==========================================================

HIGH_PRIORITY = [

    "policy",

    "government",

    "cabinet",

    "budget",

    "court",

    "supreme court",

    "high court",

    "industrial accident",

    "fire",

    "flood",

    "cyclone",

    "earthquake",

    "chemical leak",

    "power outage",

    "strike",

    "shutdown"

]

MEDIUM_PRIORITY = [

    "investment",

    "manufacturing",

    "factory",

    "employment",

    "recruitment",

    "skill",

    "training",

    "road",

    "bridge",

    "port",

    "logistics",

    "export",

    "import",

    "warehouse"

]

# ==========================================================
# REGION KEYWORDS
# ==========================================================

STATE_KEYWORDS = [

    "tamil nadu",

    "chennai",

    "sipcot",

    "sidco",

    "collector",

    "district",

    "tangedco",

    "tneb",

    "ulundurpet"

]

NATIONAL_KEYWORDS = [

    "india",

    "union",

    "parliament",

    "ministry",

    "cabinet",

    "reserve bank",

    "rbi"

]

GLOBAL_KEYWORDS = [

    "usa",

    "china",

    "vietnam",

    "bangladesh",

    "wto",

    "fta",

    "rcep",

    "cepa",

    "europe",

    "global"

]

# ==========================================================
# FIND CATEGORY
# ==========================================================

def find_categories(text):

    categories = []

    text = clean_text(text)

    for category, keywords in CATEGORY_MAPPING.items():

        for keyword in keywords:

            if clean_text(keyword) in text:

                if category not in categories:

                    categories.append(category)

    if not categories:

        categories.append("General")

    return categories

# ==========================================================
# FIND DEPARTMENTS
# ==========================================================

def find_departments(text):

    departments = []

    text = clean_text(text)

    for department, keywords in DEPARTMENT_MAPPING.items():

        for keyword in keywords:

            if clean_text(keyword) in text:

                if department not in departments:

                    departments.append(department)

    if not departments:

        departments.append("General")

    return departments
    # ==========================================================
# DETECT REGION
# ==========================================================

def detect_region(text):

    """
    Detect whether the article belongs to

    State

    National

    Global
    """

    text = clean_text(text)

    for keyword in STATE_KEYWORDS:

        if clean_text(keyword) in text:

            return "State"

    for keyword in NATIONAL_KEYWORDS:

        if clean_text(keyword) in text:

            return "National"

    for keyword in GLOBAL_KEYWORDS:

        if clean_text(keyword) in text:

            return "Global"

    return "General"


# ==========================================================
# DETECT PRIORITY
# ==========================================================

def detect_priority(text):

    """
    High

    Medium

    Low
    """

    text = clean_text(text)

    for keyword in HIGH_PRIORITY:

        if clean_text(keyword) in text:

            return "High"

    for keyword in MEDIUM_PRIORITY:

        if clean_text(keyword) in text:

            return "Medium"

    return "Low"


# ==========================================================
# BUSINESS IMPACT
# ==========================================================

def business_impact(priority):

    """
    Convert priority
    to business impact
    """

    if priority == "High":

        return "High Business Impact"

    if priority == "Medium":

        return "Moderate Business Impact"

    return "Low Business Impact"


# ==========================================================
# RISK LEVEL
# ==========================================================

def risk_level(priority):

    if priority == "High":

        return "High"

    if priority == "Medium":

        return "Medium"

    return "Low"


# ==========================================================
# URGENCY
# ==========================================================

def urgency(priority):

    if priority == "High":

        return "Immediate"

    if priority == "Medium":

        return "Monitor"

    return "Routine"


# ==========================================================
# DEPARTMENT IMPACT SCORE
# ==========================================================

def department_score(departments):

    """
    Score based on
    affected departments.
    """

    if "Public Affairs" in departments:

        return 10

    if "Engineering" in departments:

        return 9

    if "HR" in departments:

        return 8

    if "Finance" in departments:

        return 8

    if "Legal" in departments:

        return 7

    if "GSCM" in departments:

        return 7

    if "IT" in departments:

        return 6

    if "EHS" in departments:

        return 9

    return 5


# ==========================================================
# ENRICH ARTICLE
# ==========================================================

def enrich_article(article):

    """
    Add classification
    fields to article.
    """

    text = article["title"]

    if article.get("summary"):

        text += " " + article["summary"]

    categories = find_categories(text)

    departments = find_departments(text)

    priority = detect_priority(text)

    region = detect_region(text)

    article["categories"] = categories

    article["departments"] = departments

    article["priority"] = priority

    article["region"] = region

    article["business_impact"] = business_impact(priority)

    article["risk_level"] = risk_level(priority)

    article["urgency"] = urgency(priority)

    article["department_score"] = department_score(departments)

    return article
    # ==========================================================
# CATEGORIZE NEWS
# ==========================================================

def categorize_news(news):

    """
    Categorize all articles.
    """

    logger.info("Categorizing Articles...")

    categorized = []

    for article in news:

        try:

            article = enrich_article(article)

            categorized.append(article)

        except Exception as error:

            logger.warning(

                "Unable to categorize article : %s",

                error

            )

    logger.info(

        "Categorized Articles : %s",

        len(categorized)

    )

    return categorized


# ==========================================================
# CATEGORY STATISTICS
# ==========================================================

def category_statistics(news):

    stats = {}

    for article in news:

        for category in article["categories"]:

            stats[category] = stats.get(category, 0) + 1

    return dict(

        sorted(

            stats.items(),

            key=lambda x: x[1],

            reverse=True

        )

    )


# ==========================================================
# DEPARTMENT STATISTICS
# ==========================================================

def department_statistics(news):

    stats = {}

    for article in news:

        for department in article["departments"]:

            stats[department] = stats.get(

                department,

                0

            ) + 1

    return dict(

        sorted(

            stats.items(),

            key=lambda x: x[1],

            reverse=True

        )

    )


# ==========================================================
# PRIORITY STATISTICS
# ==========================================================

def priority_statistics(news):

    stats = {

        "High": 0,

        "Medium": 0,

        "Low": 0

    }

    for article in news:

        stats[

            article["priority"]

        ] += 1

    return stats


# ==========================================================
# REGION STATISTICS
# ==========================================================

def region_statistics(news):

    stats = {

        "State": 0,

        "National": 0,

        "Global": 0,

        "General": 0

    }

    for article in news:

        region = article["region"]

        if region not in stats:

            stats[region] = 0

        stats[region] += 1

    return stats


# ==========================================================
# SORT ARTICLES
# ==========================================================

def sort_articles(news):

    """
    Sort by

    1. Priority

    2. Department Score

    3. Existing News Score
    """

    priority_order = {

        "High": 3,

        "Medium": 2,

        "Low": 1

    }

    return sorted(

        news,

        key=lambda article:(

            priority_order.get(

                article["priority"],

                0

            ),

            article.get(

                "department_score",

                0

            ),

            article.get(

                "score",

                0

            )

        ),

        reverse=True

    )


# ==========================================================
# PRINT STATISTICS
# ==========================================================

def print_statistics(news):

    logger.info("")

    logger.info("=" * 60)

    logger.info("Categorization Statistics")

    logger.info("=" * 60)

    logger.info("")

    logger.info(

        "Category Statistics"

    )

    for key, value in category_statistics(news).items():

        logger.info(

            "%-35s %s",

            key,

            value

        )

    logger.info("")

    logger.info(

        "Department Statistics"

    )

    for key, value in department_statistics(news).items():

        logger.info(

            "%-35s %s",

            key,

            value

        )

    logger.info("")

    logger.info(

        "Priority Statistics"

    )

    for key, value in priority_statistics(news).items():

        logger.info(

            "%-35s %s",

            key,

            value

        )

    logger.info("")

    logger.info(

        "Region Statistics"

    )

    for key, value in region_statistics(news).items():

        logger.info(

            "%-35s %s",

            key,

            value

        )

    logger.info("=" * 60)
    # ==========================================================
# EXPORT CATEGORIZED NEWS
# ==========================================================

def export_categorized_news(news, filename="categorized_news.json"):

    """
    Export categorized news.
    """

    import json

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

            "Categorized news exported : %s",

            filename

        )

    except Exception as error:

        logger.error(

            "Export failed : %s",

            error

        )


# ==========================================================
# SEARCH NEWS
# ==========================================================

def search_news(news, keyword):

    keyword = clean_text(keyword)

    results = []

    for article in news:

        text = (

            article["title"]

            + " "

            + article.get("summary", "")

        )

        text = clean_text(text)

        if keyword in text:

            results.append(article)

    return results


# ==========================================================
# FILTER BY REGION
# ==========================================================

def filter_region(news, region):

    return [

        article

        for article in news

        if article["region"].lower()

        == region.lower()

    ]


# ==========================================================
# FILTER BY PRIORITY
# ==========================================================

def filter_priority(news, priority):

    return [

        article

        for article in news

        if article["priority"].lower()

        == priority.lower()

    ]


# ==========================================================
# FILTER BY DEPARTMENT
# ==========================================================

def filter_department(news, department):

    results = []

    for article in news:

        if department in article["departments"]:

            results.append(article)

    return results


# ==========================================================
# FILTER BY CATEGORY
# ==========================================================

def filter_category(news, category):

    results = []

    for article in news:

        if category in article["categories"]:

            results.append(article)

    return results


# ==========================================================
# SAMPLE OUTPUT
# ==========================================================

def print_sample(news, limit=10):

    logger.info("")

    logger.info("=" * 70)

    logger.info("Sample Categorized Articles")

    logger.info("=" * 70)

    for index, article in enumerate(news[:limit], start=1):

        logger.info(

            "%s. %s",

            index,

            article["title"]

        )

        logger.info(

            "Region      : %s",

            article["region"]

        )

        logger.info(

            "Priority    : %s",

            article["priority"]

        )

        logger.info(

            "Categories  : %s",

            ", ".join(

                article["categories"]

            )

        )

        logger.info(

            "Departments : %s",

            ", ".join(

                article["departments"]

            )

        )

        logger.info(

            "Impact      : %s",

            article["business_impact"]

        )

        logger.info(

            "Urgency     : %s",

            article["urgency"]

        )

        logger.info("-" * 70)


# ==========================================================
# MAIN TEST
# ==========================================================

if __name__ == "__main__":

    from fetch_news import fetch_all_news

    logger.info("")

    logger.info("=" * 70)

    logger.info("News Categorizer Engine")

    logger.info("=" * 70)

    try:

        news = fetch_all_news()

        news = categorize_news(news)

        news = sort_articles(news)

        print_statistics(news)

        print_sample(news)

        export_categorized_news(news)

        logger.info("")

        logger.info(

            "Categorizer Completed Successfully."

        )

    except Exception as error:

        logger.exception(

            "Categorizer Failed : %s",

            error

        )
