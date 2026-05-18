import pandas as pd
import matplotlib.pyplot as plt

print("Visualization started...")

# Load datasets
cbe = pd.read_csv("data/processed/cbe_sentiment.csv")
dashen = pd.read_csv("data/processed/dashen_clean.csv")
boa = pd.read_csv("data/processed/boa_clean.csv")

# Add bank labels
cbe["bank"] = "CBE"
dashen["bank"] = "Dashen"
boa["bank"] = "BOA"

# -----------------------------
# STANDARDIZE missing columns
# -----------------------------
for df in [dashen, boa]:
    if "sentiment" not in df.columns:
        df["sentiment"] = "unknown"
    if "confidence" not in df.columns:
        df["confidence"] = 0

# Ensure CBE also safe copy
if "sentiment" not in cbe.columns:
    cbe["sentiment"] = "unknown"
if "confidence" not in cbe.columns:
    cbe["confidence"] = 0

# Combine all
df = pd.concat([cbe, dashen, boa], ignore_index=True)

print("Combined dataset ready")

# -----------------------------
# 1. Sentiment distribution
# -----------------------------
sentiment_counts = df.groupby(["bank", "sentiment"]).size().unstack(fill_value=0)

sentiment_counts.plot(kind="bar")
plt.title("Sentiment Distribution by Bank")
plt.tight_layout()
plt.savefig("data/processed/sentiment_distribution.png")
plt.close()

print("Sentiment chart saved")

# -----------------------------
# 2. Average confidence
# -----------------------------
df.groupby("bank")["confidence"].mean().plot(kind="bar")

plt.title("Average Sentiment Confidence")
plt.tight_layout()
plt.savefig("data/processed/average_confidence.png")
plt.close()

print("Confidence chart saved")

# -----------------------------
# 3. Ratings distribution
# -----------------------------
df.groupby(["bank", "rating"]).size().unstack(fill_value=0).T.plot(kind="bar")

plt.title("Ratings Distribution")
plt.tight_layout()
plt.savefig("data/processed/rating_distribution.png")
plt.close()

print("Rating chart saved")

print("DONE - all visualizations generated")