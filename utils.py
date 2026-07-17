"""
===========================================================
Public Affairs Daily Intelligence Portal
Utility Functions
Version : 1.0
===========================================================
"""

import json
import re
from pathlib import Path
from datetime import datetime, timedelta
from difflib import SequenceMatcher


# ===========================================================
# PROJECT PATH
# ===========================================================

BASE_DIR = Path(__file__).resolve().parent


# ===========================================================
# DATA PATH
# ===========================================================

DATA_DIR = BASE_DIR / "data"


# ===========================================================
# CURRENT TIME
# ===========================================================

def current_time():

    return datetime.now()


# ===========================================================
# NEWS WINDOW
# ===========================================================

def within_news_window(
        published_date,
        hours
):

    limit = current_time() - timedelta(hours=hours)

    return published_date >= limit


# ===========================================================
# CLEAN TEXT
# ===========================================================

def clean_text(text):

    if text is None:
        return ""

    text = text.lower()

    text = re.sub(r"\s+", " ", text)

    text = re.sub(r"[^\w\s]", "", text)

    return text.strip()


# ===========================================================
# TITLE SIMILARITY
# ===========================================================

def similarity(title1, title2):

    return SequenceMatcher(

        None,

        clean_text(title1),

        clean_text(title2)

    ).ratio()


# ===========================================================
# JSON READER
# ===========================================================

def read_json(filename):

    filepath = DATA_DIR / filename

    if not filepath.exists():

        return None

    with open(
            filepath,
            "r",
            encoding="utf-8"
    ) as file:

        return json.load(file)


# ===========================================================
# JSON WRITER
# ===========================================================

def write_json(
        filename,
        data
):

    filepath = DATA_DIR / filename

    with open(
            filepath,
            "w",
            encoding="utf-8"
    ) as file:

        json.dump(

            data,

            file,

            indent=4,

            ensure_ascii=False

        )


# ===========================================================
# LOG
# ===========================================================

def log(message):

    print(

        "[{}] {}".format(

            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            message

        )

    )


# ===========================================================
# TEST
# ===========================================================

if __name__ == "__main__":

    log("Utility Module Loaded")

    print()

    print(

        similarity(

            "Tamil Nadu Government launches new policy",

            "TN Government launches new industrial policy"

        )

    )
