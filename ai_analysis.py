"""
==============================================================
Public Affairs Daily Intelligence Portal
Module : AI Analysis Engine
Version : 2.0
Author : Iniyaan
==============================================================
"""

import json
import logging
import os
import time

import google.generativeai as genai

# ==========================================================
# LOGGER
# ==========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# ==========================================================
# GEMINI CONFIGURATION
# ==========================================================

API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:

    genai.configure(api_key=API_KEY)

    MODEL = genai.GenerativeModel("gemini-2.5-flash")

else:

    MODEL = None

    logger.warning(

        "GEMINI_API_KEY not found."

    )

# ==========================================================
# PROMPT
# ==========================================================

PROMPT = """
You are a Senior Public Affairs Intelligence Analyst.

Analyze the following news article.

Return ONLY valid JSON.

Required JSON format:

{
  "summary":"",
  "problem":"",
  "government_impact":"",
  "business_impact":"",
  "recommendation":"",
  "urgency":"High|Medium|Low",
  "confidence":0.95
}

Do not return markdown.

Article
========
"""

# ==========================================================
# EMPTY RESPONSE
# ==========================================================

def empty_analysis():

    return {

        "summary":"",

        "problem":"",

        "government_impact":"",

        "business_impact":"",

        "recommendation":"",

        "urgency":"Medium",

        "confidence":0.0

    }

# ==========================================================
# CLEAN RESPONSE
# ==========================================================

def clean_response(text):

    text = text.strip()

    text = text.replace("```json","")

    text = text.replace("```","")

    return text.strip()

# ==========================================================
# AI REQUEST
# ==========================================================

def analyze_article(article):

    """
    Analyze one article using Gemini.
    """

    if MODEL is None:

        return empty_analysis()

    prompt = (

        PROMPT

        + "\nTitle:\n"

        + article["title"]

        + "\n\nSummary:\n"

        + article.get(

            "summary",

            ""

        )

    )

    try:

        response = MODEL.generate_content(

            prompt

        )

        result = clean_response(

            response.text

        )

        return json.loads(result)

    except Exception as error:

        logger.warning(

            "Gemini Error : %s",

            error

        )

        return empty_analysis()
        # ==========================================================
# VALIDATE AI RESPONSE
# ==========================================================

def validate_response(result):

    """
    Ensure all required fields exist.
    """

    defaults = empty_analysis()

    if not isinstance(result, dict):
        return defaults

    for key, value in defaults.items():

        if key not in result:

            result[key] = value

    # Confidence validation

    try:

        confidence = float(result["confidence"])

        confidence = max(0.0, min(1.0, confidence))

        result["confidence"] = confidence

    except Exception:

        result["confidence"] = 0.0

    # Urgency validation

    urgency = str(result["urgency"]).capitalize()

    if urgency not in ["High", "Medium", "Low"]:

        urgency = "Medium"

    result["urgency"] = urgency

    return result


# ==========================================================
# ANALYZE WITH RETRY
# ==========================================================

def analyze_with_retry(article, retry=3):

    """
    Retry Gemini request if it fails.
    """

    for attempt in range(retry):

        try:

            result = analyze_article(article)

            result = validate_response(result)

            return result

        except Exception as error:

            logger.warning(

                "Retry %s Failed : %s",

                attempt + 1,

                error

            )

            time.sleep(2)

    return empty_analysis()


# ==========================================================
# ENRICH ARTICLE
# ==========================================================

def enrich_article(article):

    """
    Add AI analysis to article.
    """

    logger.info(

        "Analyzing : %s",

        article["title"]

    )

    analysis = analyze_with_retry(article)

    article.update(analysis)

    return article


# ==========================================================
# ANALYZE ALL NEWS
# ==========================================================

def analyze_news(news):

    """
    Analyze every article.
    """

    logger.info("")

    logger.info("=" * 60)

    logger.info("AI Analysis Started")

    logger.info("=" * 60)

    analyzed = []

    for index, article in enumerate(news, start=1):

        logger.info(

            "[%s/%s] %s",

            index,

            len(news),

            article["title"]

        )

        article = enrich_article(article)

        analyzed.append(article)

        # Prevent API rate limiting
        time.sleep(1)

    logger.info("")

    logger.info("AI Analysis Completed")

    return analyzed


# ==========================================================
# AI STATISTICS
# ==========================================================

def ai_statistics(news):

    stats = {

        "High": 0,

        "Medium": 0,

        "Low": 0

    }

    total_confidence = 0

    for article in news:

        urgency = article.get(

            "urgency",

            "Medium"

        )

        stats[urgency] += 1

        total_confidence += article.get(

            "confidence",

            0

        )

    if len(news):

        stats["Average Confidence"] = round(

            total_confidence / len(news),

            2

        )

    else:

        stats["Average Confidence"] = 0

    return stats
    # ==========================================================
# EXPORT ANALYZED NEWS
# ==========================================================

def export_analysis(news, filename="analyzed_news.json"):

    """
    Export AI analyzed news.
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

            "Analysis exported : %s",

            filename

        )

    except Exception as error:

        logger.error(

            "Export Error : %s",

            error

        )


# ==========================================================
# SEARCH NEWS
# ==========================================================

def search_news(news, keyword):

    keyword = keyword.lower()

    results = []

    for article in news:

        text = (

            article["title"]

            + " "

            + article.get("summary", "")

            + " "

            + article.get("problem", "")

            + " "

            + article.get("recommendation", "")

        ).lower()

        if keyword in text:

            results.append(article)

    return results


# ==========================================================
# FILTER BY URGENCY
# ==========================================================

def filter_urgency(news, urgency):

    urgency = urgency.capitalize()

    return [

        article

        for article in news

        if article.get(

            "urgency",

            "Medium"

        ) == urgency

    ]


# ==========================================================
# FILTER BY CONFIDENCE
# ==========================================================

def filter_confidence(news, minimum=0.80):

    return [

        article

        for article in news

        if article.get(

            "confidence",

            0

        ) >= minimum

    ]


# ==========================================================
# SORT ARTICLES
# ==========================================================

def sort_articles(news):

    """
    Sort by

    1. Urgency

    2. Confidence

    3. Existing News Score
    """

    urgency_rank = {

        "High": 3,

        "Medium": 2,

        "Low": 1

    }

    return sorted(

        news,

        key=lambda article:(

            urgency_rank.get(

                article.get(

                    "urgency",

                    "Medium"

                ),

                2

            ),

            article.get(

                "confidence",

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
# PRINT AI STATISTICS
# ==========================================================

def print_statistics(news):

    stats = ai_statistics(news)

    logger.info("")

    logger.info("=" * 60)

    logger.info("AI Analysis Statistics")

    logger.info("=" * 60)

    logger.info(

        "High Urgency     : %s",

        stats["High"]

    )

    logger.info(

        "Medium Urgency   : %s",

        stats["Medium"]

    )

    logger.info(

        "Low Urgency      : %s",

        stats["Low"]

    )

    logger.info(

        "Average Confidence : %.2f",

        stats["Average Confidence"]

    )

    logger.info("=" * 60)
    # ==========================================================
# FILTER BY DEPARTMENT
# ==========================================================

def filter_department(news, department):

    """
    Filter articles by affected department.
    """

    department = department.lower()

    results = []

    for article in news:

        departments = [

            d.lower()

            for d in article.get(

                "departments",

                []

            )

        ]

        if department in departments:

            results.append(article)

    return results


# ==========================================================
# FILTER BY CATEGORY
# ==========================================================

def filter_category(news, category):

    """
    Filter by category.
    """

    category = category.lower()

    results = []

    for article in news:

        categories = [

            c.lower()

            for c in article.get(

                "categories",

                []

            )

        ]

        if category in categories:

            results.append(article)

    return results


# ==========================================================
# SAMPLE OUTPUT
# ==========================================================

def print_sample(news, limit=10):

    logger.info("")

    logger.info("=" * 70)

    logger.info("Sample AI Analysis")

    logger.info("=" * 70)

    for index, article in enumerate(news[:limit], start=1):

        logger.info(

            "%s. %s",

            index,

            article["title"]

        )

        logger.info(

            "Summary : %s",

            article.get(

                "summary",

                ""

            )

        )

        logger.info(

            "Problem : %s",

            article.get(

                "problem",

                ""

            )

        )

        logger.info(

            "Government Impact : %s",

            article.get(

                "government_impact",

                ""

            )

        )

        logger.info(

            "Business Impact : %s",

            article.get(

                "business_impact",

                ""

            )

        )

        logger.info(

            "Recommendation : %s",

            article.get(

                "recommendation",

                ""

            )

        )

        logger.info(

            "Urgency : %s",

            article.get(

                "urgency",

                "Medium"

            )

        )

        logger.info(

            "Confidence : %.2f",

            article.get(

                "confidence",

                0

            )

        )

        logger.info("-" * 70)


# ==========================================================
# MAIN TEST
# ==========================================================

if __name__ == "__main__":

    from fetch_news import fetch_all_news
    from deduplicate import process_news
    from categorizer import (
        categorize_news,
        sort_articles
    )

    logger.info("")

    logger.info("=" * 70)

    logger.info("AI Analysis Engine")

    logger.info("=" * 70)

    try:

        # Step 1 - Fetch

        news = fetch_all_news()

        # Step 2 - Remove duplicates

        news = process_news(news)

        # Step 3 - Categorize

        news = categorize_news(news)

        news = sort_articles(news)

        # Step 4 - AI Analysis

        news = analyze_news(news)

        news = sort_articles(news)

        # Step 5 - Display

        print_statistics(news)

        print_sample(news)

        export_analysis(news)

        logger.info("")

        logger.info("=" * 70)

        logger.info("AI Analysis Completed Successfully")

        logger.info("=" * 70)

    except Exception as error:

        logger.exception(

            "AI Analysis Failed : %s",

            error

        )
