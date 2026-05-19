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

# BANK MAPPING 
# (Matches the logic in your CSV and DB IDs)
# -----------------------------
def get_bank_id(bank_name):
    name = str(bank_name).lower()
    if 'commercial' in name or 'cbe' in name:
        return 1
    elif 'abyssinia' in name or 'boa' in name:
        return 2
    elif 'dashen' in name:
        return 3
    return None

# -----------------------------
# INSERT QUERY (Updated to table 'reviews3')

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


    identified_theme,
    language
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

# -----------------------------
# CONNECT DB
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

=======
    for file_path in FILES:
        print(f"Loading {file_path}...")

        df = pd.read_csv(file_path)

        # Normalize column names to lowercase
        df.columns = df.columns.str.lower().str.strip()
        
        # Replace NaN with None for SQL NULL compatibility
        df = df.where(pd.notnull(df), None)

        records = []
        for _, row in df.iterrows():
            # Extract bank name and get the corresponding ID
            csv_bank_name = row.get("bank", "")
            bank_id = get_bank_id(csv_bank_name)

            records.append((
                bank_id,
                row.get("review"),           # CSV: review -> DB: review_text
                row.get("rating"),
                row.get("date"),             # CSV: date -> DB: review_date
                row.get("sentiment_label"),
                row.get("sentiment_score"),
                row.get("identified_theme"),
                row.get("language", "en")
            ))

        # Filter out records where bank_id couldn't be determined
        valid_records = [r for r in records if r[0] is not None]

        if valid_records:
            cur.executemany(INSERT_QUERY, valid_records)
            conn.commit()
            total += len(valid_records)
            print(f"✅ Successfully inserted {len(valid_records)} rows from {file_path}")
        else:
            print(f"⚠️ No valid bank IDs found in {file_path}")

    print(f"\n🚀 DONE. Total rows inserted into 'reviews3': {total}")

except Exception as e:
    conn.rollback()
    print("❌ Error:", e)

finally:
    cur.close()
>>>>>>> 2f4330a (Reorganize project structure)
    conn.close()
