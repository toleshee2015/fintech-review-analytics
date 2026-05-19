import os
import pandas as pd

print("PREPROCESS RUNNING")

<<<<<<< HEAD
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
=======
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM reviews"))
        print("Total reviews:", result.fetchone()[0])
>>>>>>> 696bbd1df31d4ad151c48da269026ac88de00c26

RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
OUT_DIR = os.path.join(BASE_DIR, "data", "processed")

os.makedirs(OUT_DIR, exist_ok=True)

files = {
    "cbe": "commercial_bank_of_ethiopia_reviews.csv",
    "boa": "bank_of_abyssinia_reviews.csv",
    "dashen": "dashen_bank_reviews.csv"
}

for name, file in files.items():
    path = os.path.join(RAW_DIR, file)

    print("Reading:", path)

    if not os.path.exists(path):
        raise FileNotFoundError(path)

    df = pd.read_csv(path)

    out_path = os.path.join(OUT_DIR, f"{name}_clean.csv")
    df.to_csv(out_path, index=False)

    print("Saved:", out_path)

print("DONE")