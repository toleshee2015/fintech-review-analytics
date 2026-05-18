import os
import pandas as pd

print("PREPROCESS STARTED")

# ================= ROOT =================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
OUT_DIR = os.path.join(BASE_DIR, "data", "processed")

os.makedirs(OUT_DIR, exist_ok=True)

# ================= INPUT FILES =================
files = {
    "commercial bank of ethiopia": os.path.join(RAW_DIR, "commercial_bank_of_ethiopia_reviews.csv"),
    "bank of abyssinia": os.path.join(RAW_DIR, "bank_of_abyssinia_reviews.csv"),
    "dashen bank": os.path.join(RAW_DIR, "dashen_bank_reviews.csv")
}

# ================= PROCESS =================
for bank, path in files.items():
    print(f"Reading: {path}")

    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing RAW file: {path}")

    df = pd.read_csv(path)

    df["bank"] = bank

    # basic cleanup
    if "review" not in df.columns:
        df = df.rename(columns={df.columns[0]: "review"})

    if "rating" not in df.columns:
        df = df.rename(columns={df.columns[1]: "rating"})

    df = df.dropna(subset=["review", "rating"])

    output_file = os.path.join(OUT_DIR, f"{bank.replace(' ', '_')}_clean.csv")

    df.to_csv(output_file, index=False)

    print(f"Saved: {output_file}")

print("DONE")
