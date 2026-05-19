<<<<<<< HEAD
import os
import pandas as pd

print("PREPROCESS RUNNING OK")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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

    df = pd.read_csv(path)

    out_path = os.path.join(OUT_DIR, f"{name}_clean.csv")
    df.to_csv(out_path, index=False)

    print("Saved:", out_path)

print("DONE")

print("THIS FILE IS ACTIVE:", __file__)

