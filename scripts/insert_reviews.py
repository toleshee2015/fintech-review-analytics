import psycopg2
import pandas as pd
from textblob import TextBlob

# -----------------------------
# DB CONFIG
# -----------------------------
DB_CONFIG = {
    "dbname": "bank_reviews",
    "user": "postgres",
    "password": "123",
    "host": "localhost",
    "port": "5432"
}

# -----------------------------
# FILES
# -----------------------------
FILES = [
    "data/processed/cbe_clean.csv",
    "data/processed/boa_clean.csv",
    "data/processed/dashen_clean.csv"
]

# -----------------------------
# BANK MAP
# -----------------------------
BANK_MAP = {
    "commercial bank of ethiopia": 1,
    "cbe": 1,
    "bank of abyssinia": 2,
    "boa": 2,
    "dashen bank": 3,
    "dashen": 3
}

# -----------------------------
# SENTIMENT FUNCTION
# -----------------------------
def get_sentiment(text):
    score = TextBlob(str(text)).sentiment.polarity

    if score > 0:
        return "positive", score
    elif score < 0:
        return "negative", score
    else:
        return "neutral", score

# -----------------------------
# THEME EXTRACTION
# -----------------------------
def extract_theme(text):
    text = str(text).lower()

    if "otp" in text or "login" in text:
        return "authentication issue"
    elif "slow" in text or "lag" in text:
        return "performance issue"
    elif "transfer" in text or "transaction" in text:
        return "transaction service"
    elif "crash" in text or "error" in text:
        return "app crash"
    elif "easy" in text or "simple" in text:
        return "user experience"
    else:
        return "general"

# -----------------------------
# BANK ID FUNCTION
# -----------------------------
def get_bank_id(bank_name):
    name = str(bank_name).lower()

    if "commercial" in name or "cbe" in name:
        return 1
    elif "abyssinia" in name or "boa" in name:
        return 2
    elif "dashen" in name:
        return 3
    return None

# -----------------------------
# INSERT QUERY
# -----------------------------
INSERT_QUERY = """
INSERT INTO reviews3 (
    bank_id,
    review_text,
    rating,
    review_date,
    sentiment_label,
    sentiment_score,
    identified_theme,
    language
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

# -----------------------------
# MAIN PROCESS
# -----------------------------
conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

total = 0

try:
    for file_path in FILES:
        print(f"\nLoading {file_path}")

        df = pd.read_csv(file_path)
        df.columns = df.columns.str.lower().str.strip()
        df = df.where(pd.notnull(df), None)

        print("Bank names found:", df["bank"].unique())

        records = []

        for _, row in df.iterrows():
            bank_id = get_bank_id(row.get("bank"))

            if bank_id is None:
                print(f"Unknown bank: {row.get('bank')}")
                continue

            sentiment_label, sentiment_score = get_sentiment(row.get("review"))
            theme = extract_theme(row.get("review"))

            records.append((
                bank_id,
                row.get("review"),
                row.get("rating"),
                row.get("date"),
                sentiment_label,
                sentiment_score,
                theme,
                "en"
            ))

        if records:
            cur.executemany(INSERT_QUERY, records)
            conn.commit()
            total += len(records)
            print(f"Inserted {len(records)} rows")

    print(f"\nDONE. Total inserted: {total}")

except Exception as e:
    conn.rollback()
    print("Error:", e)

finally:
    cur.close()
    conn.close()
    conn.close()
>>>>>>> Stashed changes
