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

# -------------------------
# 1. Sentiment Distribution
# -------------------------
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
plt.savefig("data/processed/sentiment_distribution.png")
plt.show()

# -------------------------
# 2. Average Sentiment Score
# -------------------------
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
plt.ylabel("Average Score")

plt.tight_layout()
plt.savefig("data/processed/average_sentiment.png")
plt.show()

# -------------------------
# 3. Theme Distribution
# -------------------------
theme_counts = (
    df["identified_theme"]
    .value_counts()
)

theme_counts.plot(
    kind="bar",
    figsize=(8, 5)
)

plt.title("Theme Distribution")
plt.xlabel("Theme")
plt.ylabel("Frequency")

plt.tight_layout()
plt.savefig("data/processed/theme_distribution.png")
plt.show()

print("Visualizations completed successfully.")
