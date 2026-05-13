import pandas as pd

cbe = pd.read_csv("data/raw/commercial_bank_of_ethiopia_reviews.csv")
boa = pd.read_csv("data/raw/bank_of_abyssinia_reviews.csv")
dashen = pd.read_csv("data/raw/dashen_bank_reviews.csv")

print("CBE avg rating:", cbe["rating"].mean())
print("BOA avg rating:", boa["rating"].mean())
print("Dashen avg rating:", dashen["rating"].mean())