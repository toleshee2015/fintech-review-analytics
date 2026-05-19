import os
import pandas as pd
from textblob import TextBlob

print("PREPROCESS RUNNING OK")

# =========================================================
# BASE PATHS
# =========================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
OUT_DIR = os.path.join(BASE_DIR, "data", "processed")

os.makedirs(OUT_DIR, exist_ok=True)

# =========================================================
# INPUT FILES
# =========================================================
files = {
    "cbe": "commercial_bank_of_ethiopia_reviews.csv",
    "boa": "bank_of_abyssinia_reviews.csv",
    "dashen": "dashen_bank_reviews.csv"
}

# =========================================================
# SENTIMENT FUNCTION
# =========================================================
def get_sentiment(text):
    analysis = TextBlob(str(text))
    polarity = analysis.sentiment.polarity

    if polarity > 0:
        label = "positive"
    elif polarity < 0:
        label = "negative"
    else:
        label = "neutral"

    return label, polarity

# =========================================================
# THEME FUNCTION (simple rule-based NLP)
# =========================================================
def get_theme(text):
    text = str(text).lower()

    if "login" in text or "password" in text:
        return "login issue"
    elif "slow" in text or "loading" in text:
        return "performance issue"
    elif "crash" in text or "error" in text:
        return "app crash"
    elif "transfer" in text or "payment" in text:
        return "transaction issue"
    else:
        return "general feedback"

# =========================================================
# PROCESS EACH FILE
# =========================================================
for name, file in files.items():
    path = os.path.join(RAW_DIR, file)

    print("\nReading:", path)

    df = pd.read_csv(path)

    # -----------------------------------------------------
    # BASIC CLEANING
    # -----------------------------------------------------
    df = df.dropna(subset=["review", "rating"])
    df = df.drop_duplicates()

    # -----------------------------------------------------
    # ADD NLP FEATURES
    # -----------------------------------------------------
    df["sentiment_label"], df["sentiment_score"] = zip(
        *df["review"].apply(get_sentiment)
    )

    df["identified_theme"] = df["review"].apply(get_theme)

    # -----------------------------------------------------
    # SAVE OUTPUT
    # -----------------------------------------------------
    out_path = os.path.join(OUT_DIR, f"{name}_clean.csv")

    df.to_csv(out_path, index=False)

    print("Saved:", out_path)

print("\nDONE")
print("THIS FILE IS ACTIVE:", __file__)