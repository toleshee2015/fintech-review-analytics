import os
import pandas as pd

print("PREPROCESS STARTED:", __file__)

# ================= ROOT =================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
OUT_DIR = os.path.join(BASE_DIR, "data", "processed")

os.makedirs(OUT_DIR, exist_ok=True)

# ================= INPUT FILES =================
files = {
    "commercial_bank_of_ethiopia": os.path.join(RAW_DIR, "commercial_bank_of_ethiopia_reviews.csv"),
    "bank_of_abyssinia": os.path.join(RAW_DIR, "bank_of_abyssinia_reviews.csv"),
    "dashen_bank": os.path.join(RAW_DIR, "dashen_bank_reviews.csv")
}

# ================= PROCESS =================
all_data = []

for bank, path in files.items():
    print(f"Reading: {path}")

    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing RAW file: {path}")

    df = pd.read_csv(path)

    # normalize column names safely
    df.columns = [c.lower().strip() for c in df.columns]

    # flexible mapping (your dataset varies slightly)
    rename_map = {}

    if "review" in df.columns:
        rename_map["review"] = "review_text"
    elif "content" in df.columns:
        rename_map["content"] = "review_text"
    elif "text" in df.columns:
        rename_map["text"] = "review_text"

    if "rating" in df.columns:
        rename_map["rating"] = "rating"

    if "at" in df.columns:
        rename_map["at"] = "review_date"

    df = df.rename(columns=rename_map)

    # ensure required columns exist
    if "review_text" not in df.columns:
        raise ValueError(f"No review text column found in {path}")

    if "rating" not in df.columns:
        df["rating"] = None

    # clean
    df = df.dropna(subset=["review_text"])
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

    df["bank_name"] = bank.replace("_", " ").lower()

    all_data.append(df)

    # save per-bank file
    output_file = os.path.join(OUT_DIR, f"{bank}_clean.csv")
    df.to_csv(output_file, index=False)

    print(f"Saved: {output_file}")

# ================= OPTIONAL COMBINED FILE =================
final_df = pd.concat(all_data, ignore_index=True)

final_output = os.path.join(OUT_DIR, "all_banks_clean.csv")
final_df.to_csv(final_output, index=False)

print("DONE: preprocessing completed successfully")
