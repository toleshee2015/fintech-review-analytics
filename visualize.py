import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================================================
# LOAD DATA
# =========================================================
df = pd.read_csv("data/processed/final_reviews.csv")

df.columns = df.columns.str.lower().str.strip()

# ensure correct types
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# =========================================================
# STYLE (PUBLICATION READY)
# =========================================================
sns.set_theme(
    style="whitegrid",
    font="DejaVu Sans",
    font_scale=1.1
)

# =========================================================
# 1. SENTIMENT DISTRIBUTION BY BANK (STACKED BAR)
# =========================================================
sentiment = df.groupby(["bank", "sentiment_label"]).size().unstack(fill_value=0)

sentiment.plot(
    kind="bar",
    stacked=True,
    figsize=(10,6),
    colormap="viridis"
)

plt.title("Sentiment Distribution by Bank", fontsize=14, weight="bold")
plt.xlabel("Bank")
plt.ylabel("Number of Reviews")

plt.tight_layout()
plt.savefig("sentiment_distribution.png", dpi=300)
plt.show()

# =========================================================
# 2. RATING DISTRIBUTION (BOXPLOT)
# =========================================================
plt.figure(figsize=(10,6))

sns.boxplot(
    data=df,
    x="bank",
    y="rating",
    palette="Set2"
)

plt.title("Rating Distribution per Bank", fontsize=14, weight="bold")
plt.xlabel("Bank")
plt.ylabel("Rating (1–5)")
plt.ylim(0,5)

plt.tight_layout()
plt.savefig("rating_distribution.png", dpi=300)
plt.show()

# =========================================================
# 3. TOP THEMES (HORIZONTAL BAR CHART)
# =========================================================
plt.figure(figsize=(10,6))

theme_counts = df["identified_theme"].value_counts().head(10).reset_index()
theme_counts.columns = ["theme", "count"]

sns.barplot(
    data=theme_counts,
    x="count",
    y="theme",
    palette="Blues_r"
)

plt.title("Top Customer Issues (Themes)", fontsize=14, weight="bold")
plt.xlabel("Frequency")
plt.ylabel("Theme")

plt.tight_layout()
plt.savefig("top_themes.png", dpi=300)
plt.show()

# =========================================================
# 4. SENTIMENT TREND OVER TIME
# =========================================================
trend = df.groupby([
    pd.Grouper(key="date", freq="M"),
    "sentiment_label"
]).size().reset_index(name="count")

plt.figure(figsize=(12,6))

sns.lineplot(
    data=trend,
    x="date",
    y="count",
    hue="sentiment_label",
    marker="o"
)

plt.title("Sentiment Trend Over Time", fontsize=14, weight="bold")
plt.xlabel("Month")
plt.ylabel("Number of Reviews")

plt.tight_layout()
plt.savefig("sentiment_trend.png", dpi=300)
plt.show()

# =========================================================
# 5. AVERAGE RATING BY BANK
# =========================================================
plt.figure(figsize=(8,6))

avg_rating = df.groupby("bank")["rating"].mean().reset_index()

sns.barplot(
    data=avg_rating,
    x="bank",
    y="rating",
    palette="Set3"
)

plt.title("Average Rating by Bank", fontsize=14, weight="bold")
plt.xlabel("Bank")
plt.ylabel("Average Rating")
plt.ylim(0,5)

plt.tight_layout()
plt.savefig("avg_rating.png", dpi=300)
plt.show()