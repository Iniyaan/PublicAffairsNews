"""
============================================================
Public Affairs Daily Intelligence Portal
News Categorizer
Version 1.0
============================================================
"""

from utils import read_json

# ----------------------------------------
# Load Mapping Files
# ----------------------------------------

CATEGORY_MAPPING = read_json("category_mapping.json")

DEPARTMENT_MAPPING = read_json("department_mapping.json")


# ----------------------------------------
# Find Categories
# ----------------------------------------

def find_categories(title):

    categories = []

    title_lower = title.lower()

    for category, keywords in CATEGORY_MAPPING.items():

        for keyword in keywords:

            if keyword.lower() in title_lower:

                if category not in categories:

                    categories.append(category)

    if not categories:

        categories.append("General")

    return categories


# ----------------------------------------
# Find Departments
# ----------------------------------------

def find_departments(title):

    departments = []

    title_lower = title.lower()

    for department, keywords in DEPARTMENT_MAPPING.items():

        for keyword in keywords:

            if keyword.lower() in title_lower:

                if department not in departments:

                    departments.append(department)

    if not departments:

        departments.append("General")

    return departments


# ----------------------------------------
# Priority
# ----------------------------------------

HIGH_PRIORITY = [

    "Government",

    "Policy",

    "Cabinet",

    "Budget",

    "Court",

    "Cyclone",

    "Flood",

    "Fire",

    "Power",

    "Strike",

    "Emergency"

]


def priority(title):

    title = title.lower()

    for word in HIGH_PRIORITY:

        if word.lower() in title:

            return "High"

    return "Medium"


# ----------------------------------------
# Categorize News
# ----------------------------------------

def categorize_news(news):

    for article in news:

        article["categories"] = find_categories(

            article["title"]

        )

        article["departments"] = find_departments(

            article["title"]

        )

        article["priority"] = priority(

            article["title"]

        )

    return news


# ----------------------------------------
# Test
# ----------------------------------------

if __name__ == "__main__":

    sample = [

        {

            "title":

            "Tamil Nadu Government announces new SIPCOT Industrial Park"

        }

    ]

    output = categorize_news(sample)

    print(output)
