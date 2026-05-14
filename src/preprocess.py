import pandas as pd
import os

RAW_DIR = "data/processed"
OUT_DIR = "data/processed"

files = {
    "Commercial Bank of Ethiopia": "cbe_clean.csv",
    "Bank of Abyssinia": "boa_clean.csv",
    "Dashen Bank": "dashen_clean.csv"
}

dfs = []

for bank, file in files.items():
    path = os.path.join(RAW_DIR, file)
    df = pd.read_csv(path)

    df["bank_name"] = bank

    # standardize columns
    df = df.rename(columns={
        "review": "review_text",
        "at": "review_date"
    })

    df["source"] = "Google Play"

    # basic cleaning
    df = df.dropna(subset=["review_text", "rating"])

    dfs.append(df)

df_final = pd.concat(dfs, ignore_index=True)

output_path = os.path.join(OUT_DIR, "bank_reviews_cleaned.csv")
df_final.to_csv(output_path, index=False)

print("Preprocessing complete:", df_final.shape)