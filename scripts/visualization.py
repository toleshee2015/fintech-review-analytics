import pandas as pd
import matplotlib.pyplot as plt

# -------------------------
# Load datasets
# -------------------------
cbe = pd.read_csv("data/processed/cbe_final_dataset.csv")
boa = pd.read_csv("data/processed/boa_clean.csv")
dashen = pd.read_csv("data/processed/dashen_clean.csv")

# -------------------------
# Add bank names
# -------------------------
cbe["bank"] = "CBE"
boa["bank"] = "BOA"
dashen["bank"] = "Dashen"

# -------------------------
# Combine datasets
# -------------------------
df = pd.concat([cbe, boa, dashen])

# Create output folder
import os
os.makedirs("reports/figures", exist_ok=True)

# =========================================================
# 1. SENTIMENT DISTRIBUTION BY BANK
# =========================================================

sentiment_counts = (
    df.groupby(["bank", "sentiment_label"])
    .size()
    .unstack(fill_value=0)
)

sentiment_counts.plot(
    kind="bar",
    figsize=(8, 5)
)

plt.title("Sentiment Distribution by Bank")
plt.xlabel("Bank")
plt.ylabel("Number of Reviews")
plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig("reports/figures/sentiment_distribution.png")

plt.show()

# =========================================================
# 2. AVERAGE SENTIMENT SCORE BY BANK
# =========================================================

avg_scores = (
    df.groupby("bank")["sentiment_score"]
    .mean()
)

avg_scores.plot(
    kind="bar",
    figsize=(6, 4)
)

plt.title("Average Sentiment Score by Bank")
plt.xlabel("Bank")
plt.ylabel("Average Sentiment Score")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig("reports/figures/average_sentiment_score.png")

plt.show()

# =========================================================
# 3. RATING DISTRIBUTION BY BANK
# =========================================================

rating_counts = (
    df.groupby(["bank", "rating"])
    .size()
    .unstack(fill_value=0)
)

rating_counts.plot(
    kind="bar",
    figsize=(8, 5)
)

plt.title("Rating Distribution by Bank")
plt.xlabel("Bank")
plt.ylabel("Number of Ratings")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig("reports/figures/rating_distribution.png")

plt.show()

# =========================================================
# 4. THEME DISTRIBUTION COMPARISON
# =========================================================

theme_counts = (
    df.groupby(["bank", "identified_theme"])
    .size()
    .unstack(fill_value=0)
)

# Optional:
# keep only top 10 themes overall

top_themes = (
    df["identified_theme"]
    .value_counts()
    .head(10)
    .index
)

theme_counts = theme_counts[top_themes]

theme_counts.T.plot(
    kind="bar",
    figsize=(10, 6)
)

plt.title("Top Complaint Themes by Bank")
plt.xlabel("Theme")
plt.ylabel("Frequency")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("reports/figures/theme_distribution.png")

plt.show()

print("All visualizations generated successfully.")
