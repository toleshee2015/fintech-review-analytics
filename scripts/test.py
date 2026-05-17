import pandas as pd

file_path = "data/processed/final_reviews.csv"

df = pd.read_csv(file_path)

print("File loaded successfully")
print("Shape:", df.shape)
print("\nColumns:")
print(df.columns)
print("\nFirst 5 rows:")
print(df.head())