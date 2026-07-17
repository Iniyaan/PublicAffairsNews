"""
==========================================================
Public Affairs Daily Intelligence Portal
Configuration Loader
==========================================================
Author : Iniyaan
Version : 1.0
"""

import json
from pathlib import Path


# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"


# ==========================================================
# JSON LOADER
# ==========================================================

def load_json(filename):
    """
    Load JSON file safely.
    """

    filepath = DATA_DIR / filename

    if not filepath.exists():
        raise FileNotFoundError(f"{filename} not found.")

    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)


# ==========================================================
# LOAD CONFIGURATION FILES
# ==========================================================

SETTINGS = load_json("settings.json")

KEYWORDS = load_json("keywords.json")

WEBSITES = load_json("websites.json")

HISTORY = load_json("history.json")


# ==========================================================
# SETTINGS
# ==========================================================

PROJECT_NAME = SETTINGS["project_name"]

TIMEZONE = SETTINGS["timezone"]

UPDATE_TIME = SETTINGS["update_time"]

NEWS_WINDOW_HOURS = SETTINGS["news_window_hours"]

REMOVE_DUPLICATE_NEWS = SETTINGS["remove_duplicate_news"]

CHECK_PREVIOUS_NEWS = SETTINGS["check_previous_news"]

ARCHIVE_REPORTS = SETTINGS["archive_reports"]

GENERATE_AI_ANALYSIS = SETTINGS["generate_ai_analysis"]

GENERATE_DEPARTMENT_MAPPING = SETTINGS["generate_department_mapping"]

MINIMUM_PRIORITY = SETTINGS["minimum_priority"]

LANGUAGE = SETTINGS["language"]

MAX_RETRY = SETTINGS["max_retry"]


# ==========================================================
# FUNCTIONS
# ==========================================================

def get_keywords(category):
    """
    Return keywords for a category.
    """

    return KEYWORDS.get(category, [])


def get_websites(category):
    """
    Return websites for a category.
    """

    return WEBSITES.get(category, [])


def get_history():
    """
    Return previous news history.
    """

    return HISTORY


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)

    print(PROJECT_NAME)

    print("=" * 60)

    print()

    print("Timezone :", TIMEZONE)

    print("Update Time :", UPDATE_TIME)

    print("News Window :", NEWS_WINDOW_HOURS)

    print()

    print("State Keywords :", len(get_keywords("state")))

    print("National Keywords :", len(get_keywords("national")))

    print("Global Keywords :", len(get_keywords("global")))

    print()

    print("State Websites :", len(get_websites("state")))

    print("National Websites :", len(get_websites("national")))

    print("Global Websites :", len(get_websites("global")))

    print()

    print("History :", len(get_history()))

    print()

    print("Configuration Loaded Successfully")
