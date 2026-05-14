import psycopg2
import pandas as pd

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
    conn.close()