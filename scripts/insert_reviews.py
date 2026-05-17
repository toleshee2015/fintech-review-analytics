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
    "cbe": 1,
    "boa": 2,
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
# INSERT QUERY
# -----------------------------
INSERT_QUERY = """
INSERT INTO reviews (
    bank_id,
    review_text,
    rating,
    review_date,
    sentiment_label,
    sentiment_score
)
VALUES (%s, %s, %s, %s, %s, %s)
"""

# -----------------------------
# CONNECT DB
# -----------------------------
conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

total = 0

try:
    for file_path in FILES:
        print(f"Loading {file_path}")

        df = pd.read_csv(file_path)

        # normalize column names
        df.columns = df.columns.str.lower().str.strip()

        records = []

        for _, row in df.iterrows():
            bank_name = str(row["bank"]).lower().strip()

            sentiment_label, sentiment_score = get_sentiment(row["review"])

            records.append(
                (
                    BANK_MAP.get(bank_name),
                    row["review"],
                    row["rating"],
                    row["date"],
                    sentiment_label,
                    sentiment_score
                )
            )

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