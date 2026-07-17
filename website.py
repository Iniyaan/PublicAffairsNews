"""
============================================================
Public Affairs Daily Intelligence Portal
Website Generator
Version 1.0
============================================================
"""

from datetime import datetime


HTML_HEADER = """
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>
Public Affairs Daily Intelligence Portal
</title>

<link rel="stylesheet" href="style.css">

</head>

<body>

<header>

<h1>
Public Affairs Daily Intelligence Portal
</h1>

<p>
Daily Updated Intelligence Dashboard
</p>

</header>

<main>

"""


HTML_FOOTER = """

</main>

<footer>

<hr>

<p>

Generated Automatically

</p>

<p>

Last Updated :
{updated}

</p>

</footer>

<script src="script.js"></script>

</body>

</html>

"""


def article_card(article):

    return f"""

<div class="card">

<h2>{article['title']}</h2>

<p>

<b>Source :</b>

{article['source']}

</p>

<p>

<b>Published :</b>

{article['published']}

</p>

<p>

<b>Priority :</b>

{article['priority']}

</p>

<p>

<b>Category :</b>

{", ".join(article['categories'])}

</p>

<p>

<b>Departments :</b>

{", ".join(article['departments'])}

</p>

<p>

<b>Summary</b>

<br>

{article.get('summary','')}

</p>

<p>

<b>Problem</b>

<br>

{article.get('problem','')}

</p>

<p>

<b>Business Impact</b>

<br>

{article.get('business_impact','')}

</p>

<p>

<b>Recommended Action</b>

<br>

{article.get('recommended_action','')}

</p>

<p>

<b>Urgency :</b>

{article.get('urgency','Medium')}

</p>

<p>

<a href="{article['link']}">

Read Full Article

</a>

</p>

</div>

"""


def build_section(title, articles):

    html = f"<section><h1>{title}</h1>"

    for article in articles:

        html += article_card(article)

    html += "</section>"

    return html


def generate_website(news):

    state = []

    national = []

    global_news = []

    for article in news:

        if article["category"] == "state":

            state.append(article)

        elif article["category"] == "national":

            national.append(article)

        else:

            global_news.append(article)

    html = HTML_HEADER

    html += f"""

<section>

<h2>

Today's Summary

</h2>

<p>

State Articles :
{len(state)}

</p>

<p>

National Articles :
{len(national)}

</p>

<p>

Global Articles :
{len(global_news)}

</p>

<p>

Total Articles :
{len(news)}

</p>

</section>

"""

    html += build_section(

        "Tamil Nadu Public Affairs",

        state

    )

    html += build_section(

        "India Public Affairs",

        national

    )

    html += build_section(

        "Global Public Affairs",

        global_news

    )

    html += HTML_FOOTER.format(

        updated=datetime.now().strftime(

            "%d-%m-%Y %I:%M %p"

        )

    )

    with open(

        "index.html",

        "w",

        encoding="utf-8"

    ) as file:

        file.write(html)

    print(

        "Website Generated Successfully."

    )
