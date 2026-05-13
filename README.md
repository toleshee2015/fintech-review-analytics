## 📌 Overview

This project analyzes user reviews of Ethiopian banking mobile applications using data scraped from the Google Play Store. The goal is to compare customer satisfaction, identify common issues, and extract insights across multiple banking apps.

Banks analyzed:
- Commercial Bank of Ethiopia (CBE)
- Bank of Abyssinia (BOA)
- Dashen Bank

---

## 🎯 Objectives

- Collect real-world user feedback from mobile banking apps
- Clean and preprocess raw review data
- Compare customer satisfaction across banks
- Identify common user complaints and trends
- Prepare dataset for sentiment analysis and NLP tasks

---

---

## ⚙️ Tech Stack

- Python 🐍
- Pandas 📊
- Google Play Scraper 📱
- Matplotlib 📈
- Jupyter Notebook 📓

---

## 📥 Data Collection Methodology

Data was collected using the `google-play-scraper` Python library.

### 🔧 Scraping Configuration:
- Language: English (`en`)
- Country: Ethiopia (`et`)
- Sorting: Most recent reviews (`Sort.NEWEST`)
- Pagination enabled for extended collection

### 📦 Data Fields:
- Review text
- Rating (1–5 stars)
- Review date
- Bank name
- Source (Google Play Store)

---

## 🧹 Data Preprocessing

The dataset was cleaned using the following steps:

- Removal of missing values (review text & rating)
- Duplicate removal using `review_id` (hash-based ID)
- Date normalization to `YYYY-MM-DD`
- Standardized column structure across all banks
- Separate cleaned datasets per bank

---Date_range---
01/10/2024-12/05/2026

#################
## 🏗️ Project Structure
fintech-review-analytics/
│
├── data/
│ ├── raw/ # Raw scraped reviews (ignored in GitHub)
│ ├── processed/ # Cleaned datasets (ignored in GitHub)
│
├── notebooks/ # Jupyter notebooks for analysis
│
├── src/
│ ├── scrape_reviews.py # Google Play scraping script
│ ├── preprocess.py # Data cleaning pipeline
│ ├── analysis.py # Statistical analysis
│
├── tests/
│
├── venv/
├── requirements.txt
├── .gitignore
└── README.md

