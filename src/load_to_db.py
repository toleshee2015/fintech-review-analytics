import os
import pandas as pd
from sqlalchemy import create_engine

# ================= DATABASE =================
engine = create_engine(
    "postgresql://postgres:123@localhost:5432/bank_reviews"
)

# ================= PROJECT ROOT PATH =================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ================= INPUT FILES =================
files = {
    "commercial bank of ethiopia": os.path.join(BASE_DIR, "data", "processed", "cbe_clean.csv"),
    "bank of abyssinia": os.path.join(BASE_DIR, "data", "processed", "boa_clean.csv"),
    "dashen bank": os.path.join(BASE_DIR, "data", "processed", "dashen_clean.csv")
}

# ================= LOAD + COMBINE DATA =================
dfs = []

print("Loading files...")

for bank, path in files.items():
    print(f"Reading: {path}")

    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")

    df = pd.read_csv(path)

    df["bank_name"] = bank
    dfs.append(df)

df = pd.concat(dfs, ignore_index=True)

print("After concat:", df.shape)

# ================= NORMALIZE =================
df["bank_name"] = df["bank_name"].str.strip().str.lower()

# standard column mapping
df = df.rename(columns={
    "review": "review_text",
    "date": "review_date"
})

# ================= LOAD BANK TABLE =================
banks = pd.read_sql("SELECT bank_id, bank_name FROM banks", engine)
banks["bank_name"] = banks["bank_name"].str.strip().str.lower()

# ================= MERGE =================
df = df.merge(banks, on="bank_name", how="inner")

print("After merge:", df.shape)

# ================= VALIDATION =================
required_cols = ["bank_id", "review_text", "rating"]

missing = [c for c in required_cols if c not in df.columns]
if missing:
    raise Exception(f"Missing columns: {missing}")

df_final = df[required_cols].copy()

# clean rating
df_final["rating"] = pd.to_numeric(df_final["rating"], errors="coerce")
df_final = df_final.dropna(subset=["review_text", "rating"])
df_final["rating"] = df_final["rating"].astype(int)

print("Final rows to insert:", len(df_final))

# ================= INSERT INTO POSTGRESQL =================
df_final.to_sql(
    "reviews",
    engine,
    if_exists="append",
    index=False,
    method="multi"
)

print("SUCCESS: Data inserted into PostgreSQL (reviews table)")
