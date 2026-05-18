import pandas as pd
import matplotlib.pyplot as plt

print("Visualization script started...")

# -----------------------------
# Load datasets
# -----------------------------
cbe = pd.read_csv("data/processed/cbe_sentiment.csv")
dashen = pd.read_csv("data/processed/dashen_clean.csv")
boa = pd.read_csv("data/processed/boa_clean.csv")

# -----------------------------
# Standardize columns
# -----------------------------
cbe["bank"] = "CBE"
dashen["bank"] = "Dashen"
boa["bank"] = "BOA"

# -----------------------------
# Combine all datasets
# -----------------------------
df = pd.concat([cbe, dashen, boa])

print("Datasets loaded successfully.")

# -----------------------------
# Chart 1: Sentiment Distribution
# -----------------------------
sentiment_counts = (
    df.groupby(["bank", "sentiment"])
    .size()
    .unstack(fill_value=0)
)

sentiment_counts.plot(kind="bar")

plt.title("Sentiment Distribution by Bank")
plt.xlabel("Bank")
plt.ylabel("Number of Reviews")

plt.tight_layout()

plt.savefig(
    "data/processed/sentiment_distribution.png"
)

print("Chart 1 saved.")

plt.close()

# -----------------------------
# Chart 2: Average Confidence
# -----------------------------
avg_scores = (
    df.groupby("bank")["confidence"]
    .mean()
)

avg_scores.plot(kind="bar")

plt.title("Average Sentiment Confidence")
plt.xlabel("Bank")
plt.ylabel("Confidence Score")

plt.tight_layout()

plt.savefig(
    "data/processed/average_sentiment_score.png"
)

print("Chart 2 saved.")

plt.close()

# -----------------------------
# Chart 3: Ratings Distribution
# -----------------------------
rating_counts = (
    df.groupby(["bank", "rating"])
    .size()
    .unstack(fill_value=0)
)

rating_counts.T.plot(kind="bar")

plt.title("Ratings Distribution")
plt.xlabel("Rating")
plt.ylabel("Review Count")

plt.tight_layout()

plt.savefig(
    "data/processed/rating_distribution.png"
)

print("Chart 3 saved.")

plt.close()

print("Visualizations generated successfully.")