from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from src.database import get_engine


engine = get_engine()

print("Connecting to database...")

# -------------------------
# Load data directly from PostgreSQL
# -------------------------
query = """
SELECT review_text, rating, review_date, bank_name, sentiment_label, sentiment_score, identified_theme
FROM reviews
JOIN banks ON reviews.bank_id = banks.bank_id
"""

df = pd.read_sql(query, engine)

print("Data loaded from DB:", df.shape)

# -------------------------
# 1. Sentiment Distribution by Bank
# -------------------------
sentiment_counts = df.groupby(["bank_name", "sentiment_label"]).size().unstack(fill_value=0)

# =========================================================
# BASE DIRECTORY
# =========================================================
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================================================
# CORRECT DATASET PATHS (FIXED)
# =========================================================
cbe_path = BASE_DIR / "data" / "processed" / "cbe_clean.csv"
boa_path = BASE_DIR / "data" / "processed" / "boa_clean.csv"
dashen_path = BASE_DIR / "data" / "processed" / "dashen_clean.csv"

# =========================================================
# LOAD DATASETS
# =========================================================
try:
    cbe = pd.read_csv(cbe_path)
    boa = pd.read_csv(boa_path)
    dashen = pd.read_csv(dashen_path)
    print("Datasets loaded successfully.")
except FileNotFoundError as e:
    print(f"File not found: {e}")
    exit()

# =========================================================
# ADD BANK LABELS
# =========================================================
cbe["bank"] = "CBE"
boa["bank"] = "BOA"
dashen["bank"] = "Dashen"

# =========================================================
# COMBINE DATASETS
# =========================================================
df = pd.concat([cbe, boa, dashen], ignore_index=True)

# =========================================================
# OUTPUT DIRECTORY
# =========================================================
figures_dir = BASE_DIR / "reports" / "figures"
os.makedirs(figures_dir, exist_ok=True)

# =========================================================
# 1. SENTIMENT DISTRIBUTION BY BANK
# =========================================================
sentiment_counts = df.groupby(["bank", "sentiment_label"]).size().unstack(fill_value=0)


sentiment_counts.plot(kind="bar", figsize=(8, 5))
plt.title("Sentiment Distribution by Bank")
plt.xlabel("Bank")
plt.ylabel("Number of Reviews")
plt.xticks(rotation=0)
plt.tight_layout()


plt.savefig("data/processed/sentiment_distribution_db.png")
plt.show()

# -------------------------
# 2. Average Sentiment Score by Bank
# -------------------------
avg_scores = df.groupby("bank_name")["sentiment_score"].mean()

plt.savefig(figures_dir / "sentiment_distribution.png")
plt.show()

# =========================================================
# 2. AVERAGE SENTIMENT SCORE BY BANK
# =========================================================
avg_scores = df.groupby("bank")["sentiment_score"].mean()
avg_scores.plot(kind="bar", figsize=(6, 4))
plt.title("Average Sentiment Score by Bank")
plt.xlabel("Bank")

plt.ylabel("Average Score")
plt.tight_layout()

plt.savefig("data/processed/avg_sentiment_db.png")
plt.show()

# -------------------------
# 3. Theme Distribution
# -------------------------
theme_counts = df["identified_theme"].value_counts()
theme_counts.plot(kind="bar", figsize=(8, 5))
plt.title("Theme Distribution (All Banks)")
plt.xlabel("Theme")
plt.ylabel("Frequency")
plt.tight_layout()

plt.savefig("data/processed/theme_distribution_db.png")
plt.show()

print("Visualizations completed from database.")

plt.ylabel("Average Sentiment Score")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(figures_dir / "average_sentiment_score.png")
plt.show()

# =========================================================
# 3. RATING DISTRIBUTION BY BANK
# =========================================================
rating_counts = df.groupby(["bank", "rating"]).size().unstack(fill_value=0)
rating_counts.plot(kind="bar", figsize=(8, 5))
plt.title("Rating Distribution by Bank")
plt.xlabel("Bank")
plt.ylabel("Number of Ratings")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(figures_dir / "rating_distribution.png")
plt.show()

# =========================================================
# 4. THEME DISTRIBUTION (TOP 10)
# =========================================================
theme_counts = df["identified_theme"].value_counts().head(10)

theme_counts.plot(kind="bar", figsize=(8, 5))
plt.title("Top 10 Complaint Themes")
plt.xlabel("Theme")
plt.ylabel("Frequency")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(figures_dir / "theme_distribution.png")
plt.show()

# =========================================================
# DONE
# =========================================================
print("All visualizations generated successfully.")
print(f"Figures saved in: {figures_dir}")

