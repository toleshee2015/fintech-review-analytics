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
