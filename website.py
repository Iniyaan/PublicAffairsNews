"""
==============================================================
Public Affairs Daily Intelligence Portal
Website Generator
==============================================================
"""

import os
from datetime import datetime

TITLE = "Public Affairs Daily Intelligence Portal"

# ----------------------------------------------------------

def html_header():

    now = datetime.now().strftime("%d-%m-%Y %I:%M %p")

    return f"""<!DOCTYPE html>
<html>
<head>

<meta charset="utf-8">

<meta name="viewport"
content="width=device-width, initial-scale=1">

<title>{TITLE}</title>

<link rel="stylesheet" href="style.css">

<script src="script.js"></script>

</head>

<body>

<header>

<h1>{TITLE}</h1>

<p>Updated : {now}</p>

</header>

<div class="container">
"""

# ----------------------------------------------------------

def html_footer():

    return """
</div>

<footer>

<p>&copy; 2026 Public Affairs Daily Intelligence Portal</p>

</footer>

</body>

</html>
"""

# ----------------------------------------------------------

def create_card(article):

    return f"""
<div class="card">

<h2>{article['title']}</h2>

<p><b>Source:</b> {article['source']}</p>

<p><b>Published:</b> {article['published']}</p>

<p>{article.get('summary','')}</p>

<p><b>Priority:</b> {article.get('priority','Low')}</p>

<p><b>Departments:</b> {", ".join(article.get("departments",[]))}</p>

<p><b>Categories:</b> {", ".join(article.get("categories",[]))}</p>

<p><a href="{article['link']}" target="_blank">
Read More
</a></p>

</div>
"""
# ----------------------------------------------------------
# FILTER FUNCTIONS
# ----------------------------------------------------------

def filter_region(news, region):

    return [

        article

        for article in news

        if article.get(

            "region",

            ""

        ).lower() == region.lower()

    ]


def filter_priority(news, priority):

    return [

        article

        for article in news

        if article.get(

            "priority",

            ""

        ).lower() == priority.lower()

    ]


# ----------------------------------------------------------
# CREATE SECTION
# ----------------------------------------------------------

def create_section(title, articles):

    html = f"""

<section>

<h2>{title}</h2>

"""

    if len(articles) == 0:

        html += """

<p>No News Available</p>

"""

    else:

        for article in articles:

            html += create_card(article)

    html += """

</section>

"""

    return html


# ----------------------------------------------------------
# DASHBOARD SUMMARY
# ----------------------------------------------------------

def dashboard_summary(news):

    total = len(news)

    state = len(filter_region(news, "State"))

    national = len(filter_region(news, "National"))

    global_news = len(filter_region(news, "Global"))

    high = len(filter_priority(news, "High"))

    medium = len(filter_priority(news, "Medium"))

    low = len(filter_priority(news, "Low"))

    return f"""

<div class="dashboard">

<div class="box">

<h3>Total News</h3>

<p>{total}</p>

</div>

<div class="box">

<h3>State</h3>

<p>{state}</p>

</div>

<div class="box">

<h3>National</h3>

<p>{national}</p>

</div>

<div class="box">

<h3>Global</h3>

<p>{global_news}</p>

</div>

<div class="box">

<h3>High Priority</h3>

<p>{high}</p>

</div>

<div class="box">

<h3>Medium Priority</h3>

<p>{medium}</p>

</div>

<div class="box">

<h3>Low Priority</h3>

<p>{low}</p>

</div>

</div>

"""


# ----------------------------------------------------------
# SEARCH BAR
# ----------------------------------------------------------

def search_bar():

    return """

<div class="search">

<input

type="text"

id="searchInput"

placeholder="Search News..."

onkeyup="searchNews()">

</div>

"""
# ----------------------------------------------------------
# HIGH PRIORITY SECTION
# ----------------------------------------------------------

def high_priority_section(news):

    return create_section(

        "🚨 High Priority Alerts",

        filter_priority(

            news,

            "High"

        )

    )


# ----------------------------------------------------------
# STATE NEWS
# ----------------------------------------------------------

def state_section(news):

    return create_section(

        "🏛 Tamil Nadu / State News",

        filter_region(

            news,

            "State"

        )

    )


# ----------------------------------------------------------
# NATIONAL NEWS
# ----------------------------------------------------------

def national_section(news):

    return create_section(

        "🇮🇳 National News",

        filter_region(

            news,

            "National"

        )

    )


# ----------------------------------------------------------
# GLOBAL NEWS
# ----------------------------------------------------------

def global_section(news):

    return create_section(

        "🌍 Global News",

        filter_region(

            news,

            "Global"

        )

    )


# ----------------------------------------------------------
# GENERATE HTML
# ----------------------------------------------------------

def generate_html(news):

    html = ""

    html += html_header()

    html += dashboard_summary(news)

    html += search_bar()

    html += high_priority_section(news)

    html += state_section(news)

    html += national_section(news)

    html += global_section(news)

    html += html_footer()

    return html


# ----------------------------------------------------------
# SAVE WEBSITE
# ----------------------------------------------------------

def save_website(news):

    html = generate_html(news)

    with open(

        "index.html",

        "w",

        encoding="utf-8"

    ) as file:

        file.write(html)

    print("index.html generated successfully.")


# ----------------------------------------------------------
# SAVE ARCHIVE
# ----------------------------------------------------------

def save_archive(news):

    if not os.path.exists("archive"):

        os.makedirs("archive")

    filename = datetime.now().strftime(

        "archive/%Y-%m-%d.html"

    )

    with open(

        filename,

        "w",

        encoding="utf-8"

    ) as file:

        file.write(

            generate_html(news)

        )

    print(

        f"{filename} created successfully."

    )
    # ----------------------------------------------------------
# BUILD DASHBOARD
# ----------------------------------------------------------

def build_dashboard(news):

    """
    Generate website files.
    """

    save_website(news)

    save_archive(news)

    print("Dashboard Generated Successfully.")


# ----------------------------------------------------------
# MAIN TEST
# ----------------------------------------------------------

if __name__ == "__main__":

    from fetch_news import fetch_all_news
    from deduplicate import process_news
    from categorizer import categorize_news, sort_articles
    from ai_analysis import analyze_news

    try:

        print("=" * 70)
        print("PUBLIC AFFAIRS DAILY INTELLIGENCE PORTAL")
        print("=" * 70)

        # STEP 1
        print("\nFetching News...")
        news = fetch_all_news()

        # STEP 2
        print("Removing Duplicates...")
        news = process_news(news)

        # STEP 3
        print("Categorizing...")
        news = categorize_news(news)
        news = sort_articles(news)

        # STEP 4
        print("Running AI Analysis...")
        news = analyze_news(news)

        # STEP 5
        print("Generating Website...")
        build_dashboard(news)

        print("\nCompleted Successfully")
        print(f"Articles Published : {len(news)}")

    except Exception as error:

        print("\nWebsite Generation Failed")

        raise error
