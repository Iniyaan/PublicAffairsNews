"""
==============================================================
Public Affairs Daily Intelligence Portal
Module : Website Generator
Version : 2.0
Author : Iniyaan
==============================================================
"""

import os
import logging
from datetime import datetime

# ==========================================================
# LOGGER
# ==========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# ==========================================================
# WEBSITE TITLE
# ==========================================================

TITLE = "Public Affairs Daily Intelligence Portal"

SUBTITLE = (
    "Government • Manufacturing • Public Affairs "
    "• Industry Intelligence"
)

# ==========================================================
# DATE
# ==========================================================

def generated_time():

    now = datetime.now()

    return now.strftime("%d-%m-%Y %I:%M %p")


# ==========================================================
# HTML HEADER
# ==========================================================

def html_header():

    return f"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta
name="viewport"
content="width=device-width, initial-scale=1.0">

<title>{TITLE}</title>

<link
rel="stylesheet"
href="style.css">

<script
src="script.js"
defer></script>

</head>

<body>

<header>

<div class="header">

<h1>{TITLE}</h1>

<p>{SUBTITLE}</p>

<p class="date">

Last Updated :
{generated_time()}

</p>

</div>

</header>

<main>
"""


# ==========================================================
# SUMMARY CARD
# ==========================================================

def summary_card(news):

    total = len(news)

    high = len(

        [

            n

            for n in news

            if n.get(

                "priority",

                ""

            ) == "High"

        ]

    )

    updated = len(

        [

            n

            for n in news

            if n.get(

                "updated",

                False

            )

        ]

    )

    return f"""

<section>

<h2>Today's Summary</h2>

<div class="summary-grid">

<div class="summary-card">

<h3>Total News</h3>

<p>{total}</p>

</div>

<div class="summary-card">

<h3>High Priority</h3>

<p>{high}</p>

</div>

<div class="summary-card">

<h3>Updated Stories</h3>

<p>{updated}</p>

</div>

</div>

</section>

"""


# ==========================================================
# SECTION TITLE
# ==========================================================

def section(title):

    return f"""

<section>

<h2>{title}</h2>

"""
    # ==========================================================
# PRIORITY COLOR
# ==========================================================

def priority_class(priority):

    priority = priority.lower()

    if priority == "high":

        return "priority-high"

    if priority == "medium":

        return "priority-medium"

    return "priority-low"


# ==========================================================
# CREATE NEWS CARD
# ==========================================================

def news_card(article):

    priority = article.get(

        "priority",

        "Low"

    )

    badge = priority_class(

        priority

    )

    updated = ""

    if article.get(

        "updated",

        False

    ):

        updated = """

<span class="updated">

UPDATED

</span>

"""

    departments = ""

    for department in article.get(

        "departments",

        []

    ):

        departments += f"""

<span class="department">

{department}

</span>

"""

    categories = ""

    for category in article.get(

        "categories",

        []

    ):

        categories += f"""

<span class="category">

{category}

</span>

"""

    return f"""

<div class="news-card">

<div class="card-header">

<h3>

{article['title']}

</h3>

<span class="{badge}">

{priority}

</span>

{updated}

</div>

<div class="card-body">

<p>

<strong>Source :</strong>

{article['source']}

</p>

<p>

<strong>Published :</strong>

{article['published']}

</p>

<p>

<strong>Summary :</strong>

{article.get('summary','')}

</p>

<p>

<strong>Problem :</strong>

{article.get('problem','')}

</p>

<p>

<strong>Business Impact :</strong>

{article.get('business_impact','')}

</p>

<p>

<strong>Recommendation :</strong>

{article.get('recommendation','')}

</p>

<p>

<strong>Confidence :</strong>

{article.get('confidence',0)}

</p>

<div class="category-container">

{categories}

</div>

<div class="department-container">

{departments}

</div>

<p>

<a

href="{article['link']}"

target="_blank">

Read Original News →

</a>

</p>

</div>

</div>

"""


# ==========================================================
# GENERATE NEWS SECTION
# ==========================================================

def generate_news_section(

    title,

    articles

):

    html = section(title)

    if len(articles) == 0:

        html += """

<p>

No News Available

</p>

"""

    else:

        for article in articles:

            html += news_card(

                article

            )

    html += """

</section>

"""

    return html
# ==========================================================
# FILTER ARTICLES
# ==========================================================

def filter_region(news, region):

    return [

        article

        for article in news

        if article.get(

            "region",

            ""

        ).lower()

        == region.lower()

    ]


def filter_priority(news):

    return [

        article

        for article in news

        if article.get(

            "priority",

            ""

        ) == "High"

    ]


# ==========================================================
# SEARCH BAR
# ==========================================================

def search_bar():

    return """

<section>

<div class="search-container">

<input

type="text"

id="searchInput"

placeholder="Search News..."

onkeyup="searchNews()">

</div>

</section>

"""


# ==========================================================
# DASHBOARD STATISTICS
# ==========================================================

def dashboard_statistics(news):

    state = len(filter_region(news, "State"))

    national = len(filter_region(news, "National"))

    global_news = len(filter_region(news, "Global"))

    return f"""

<section>

<div class="dashboard-grid">

<div class="dashboard-card">

<h3>State</h3>

<p>{state}</p>

</div>

<div class="dashboard-card">

<h3>National</h3>

<p>{national}</p>

</div>

<div class="dashboard-card">

<h3>Global</h3>

<p>{global_news}</p>

</div>

</div>

</section>

"""


# ==========================================================
# HIGH PRIORITY ALERTS
# ==========================================================

def high_priority_section(news):

    articles = filter_priority(news)

    return generate_news_section(

        "🚨 High Priority Alerts",

        articles

    )


# ==========================================================
# STATE NEWS
# ==========================================================

def state_news(news):

    return generate_news_section(

        "🏛 Tamil Nadu / State News",

        filter_region(

            news,

            "State"

        )

    )


# ==========================================================
# NATIONAL NEWS
# ==========================================================

def national_news(news):

    return generate_news_section(

        "🇮🇳 National News",

        filter_region(

            news,

            "National"

        )

    )


# ==========================================================
# GLOBAL NEWS
# ==========================================================

def global_news(news):

    return generate_news_section(

        "🌍 Global News",

        filter_region(

            news,

            "Global"

        )

    )


# ==========================================================
# ARCHIVE LINK
# ==========================================================

def archive_section():

    return """

<section>

<h2>Archive</h2>

<p>

Previous reports are available inside

the archive folder.

</p>

</section>

# ==========================================================
# HTML FOOTER
# ==========================================================

def html_footer():

    return """
</main>

<footer>

<p>
&copy; 2026 Public Affairs Daily Intelligence Portal
</p>

<p>
Automatically Generated by GitHub Actions
</p>

</footer>

</body>

</html>
"""

    return """

</main>

<footer>

<p>

© 2026 Public Affairs Daily Intelligence Portal

</p>

<p>

Automatically Generated by GitHub Actions

</p>

</footer>

</body>

</html>

"""


# ==========================================================
# GENERATE COMPLETE WEBSITE
# ==========================================================

def generate_website(news):

    logger.info("Generating Website...")

    html = ""

    html += html_header()

    html += summary_card(news)

    html += search_bar()

    html += dashboard_statistics(news)

    html += high_priority_section(news)

    html += state_news(news)

    html += national_news(news)

    html += global_news(news)

    html += archive_section()

    html += html_footer()

    return html


# ==========================================================
# SAVE INDEX.HTML
# ==========================================================

def save_index(news, filename="index.html"):

    html = generate_website(news)

    with open(

        filename,

        "w",

        encoding="utf-8"

    ) as file:

        file.write(html)

    logger.info(

        "Website Generated : %s",

        filename

    )


# ==========================================================
# SAVE ARCHIVE
# ==========================================================

def save_archive(news):

    if not os.path.exists("archive"):

        os.makedirs("archive")

    filename = datetime.now().strftime(

        "archive/%Y-%m-%d.html"

    )

    html = generate_website(news)

    with open(

        filename,

        "w",

        encoding="utf-8"

    ) as file:

        file.write(html)

    logger.info(

        "Archive Saved : %s",

        filename

    )


# ==========================================================
# MAIN FUNCTION
# ==========================================================

def build_dashboard(news):

    save_index(news)

    save_archive(news)


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
    from ai_analysis import analyze_news

    logger.info("=" * 70)
    logger.info("Website Generator")
    logger.info("=" * 70)

    try:

        # Fetch

        news = fetch_all_news()

        # Remove duplicates

        news = process_news(news)

        # Categorize

        news = categorize_news(news)

        news = sort_articles(news)

        # AI Analysis

        news = analyze_news(news)

        # Build Website

        build_dashboard(news)

        logger.info("")
        logger.info("=" * 70)
        logger.info("Website Generated Successfully")
        logger.info("=" * 70)

    except Exception as error:

        logger.exception(

            "Website Generation Failed : %s",

            error

        )"""

    
