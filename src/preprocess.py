import os
import pandas as pd

# ================= PATHS =================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

raw_files = {
    "commercial bank of ethiopia": os.path.join(BASE_DIR, "data", "raw", "commercial_bank_of_ethiopia_reviews.csv"),
    "bank of abyssinia": os.path.join(BASE_DIR, "data", "raw", "bank_of_abyssinia_reviews.csv"),
    "dashen bank": os.path.join(BASE_DIR, "data", "raw", "dashen_bank_reviews.csv")
}

processed_dir = os.path.join(BASE_DIR, "data", "processed")
os.makedirs(processed_dir, exist_ok=True)

# ================= PROCESS =================
for bank, path in raw_files.items():
    print(f"Processing: {path}")

    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing raw file: {path}")

    df = pd.read_csv(path)

    # standard columns
    df = df.rename(columns={
        "review": "review",
        "rating": "rating",
        "at": "date"
    })

    df["bank"] = bank

    # simple cleaning
    df = df.dropna(subset=["review", "rating"])

    # save processed file
    output_path = os.path.join(processed_dir, f"{bank.replace(' ', '_')}_clean.csv")

    df.to_csv(output_path, index=False)

    print(f"Saved: {output_path}")

print("Preprocessing completed successfully.")
