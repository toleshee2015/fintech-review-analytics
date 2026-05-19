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
    identified_theme
)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

# -----------------------------
# CONNECT TO DATABASE
# -----------------------------
conn = psycopg2.connect(**DB_CONFIG)

cur = conn.cursor()

total = 0

try:

    for file_path in FILES:

        print(f"\nLoading {file_path}")

        df = pd.read_csv(file_path)

        # normalize column names
        df.columns = df.columns.str.lower().str.strip()

        # debug bank names
        print("Bank names found:", df["bank"].unique())

        records = []

        for _, row in df.iterrows():

            # clean bank name
            bank_name = str(row["bank"]).lower().strip()

            # map to bank_id
            bank_id = BANK_MAP.get(bank_name)

            # skip unknown banks
            if bank_id is None:
                print(f"Unknown bank name: {bank_name}")
                continue

            # sentiment analysis
            sentiment_label, sentiment_score = get_sentiment(
                row["review"]
            )

            # theme extraction
            theme = extract_theme(row["review"])

            # append final record
            records.append(
                (
                    bank_id,
                    row["review"],
                    row["rating"],
                    row["date"],
                    sentiment_label,
                    sentiment_score,
                    theme
                )
            )

        # insert into PostgreSQL
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