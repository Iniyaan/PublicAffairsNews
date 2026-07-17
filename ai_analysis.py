"""
============================================================
Public Affairs Daily Intelligence Portal
Gemini AI Analysis
Version 1.0
============================================================
"""

import json
import google.generativeai as genai

from config import SETTINGS


# ------------------------------------------------------------
# Configure Gemini
# ------------------------------------------------------------

# IMPORTANT:
# Replace with environment variable later in GitHub Actions.
# For now you can temporarily place your API key here only for testing.

GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


# ------------------------------------------------------------
# Prompt
# ------------------------------------------------------------

PROMPT = """
You are a Public Affairs Intelligence Analyst.

Analyze the following news article.

Return ONLY valid JSON.

Format:

{
"summary":"",
"problem":"",
"business_impact":"",
"recommended_action":"",
"urgency":"High/Medium/Low",
"confidence":0.95
}

News:

"""


# ------------------------------------------------------------
# AI Analysis
# ------------------------------------------------------------

def analyze_article(article):

    try:

        response = model.generate_content(

            PROMPT +

            article["title"] +

            "\n\n" +

            article.get("summary","")

        )

        text = response.text.strip()

        text = text.replace("```json","")

        text = text.replace("```","")

        return json.loads(text)

    except Exception as e:

        return {

            "summary":"",

            "problem":"",

            "business_impact":"",

            "recommended_action":"",

            "urgency":"Medium",

            "confidence":0,

            "error":str(e)

        }


# ------------------------------------------------------------
# Analyze News
# ------------------------------------------------------------

def analyze_news(news):

    for article in news:

        result = analyze_article(article)

        article.update(result)

    return news


# ------------------------------------------------------------
# Test
# ------------------------------------------------------------

if __name__ == "__main__":

    sample = [

        {

            "title":"Tamil Nadu Government announces new industrial policy",

            "summary":"New industrial policy announced."

        }

    ]

    result = analyze_news(sample)

    print(result)
