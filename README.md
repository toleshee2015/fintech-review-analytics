🏦 Covered InstitutionsCommercial Bank of Ethiopia (CBE)   Bank of Abyssinia (BOA)   Dashen Bank   🛠️ System Architecture & Features[Raw App Reviews] ➔ [Data Preprocessing] ➔ [Dual-Model Sentiment Engine] ➔ [Thematic Classifier & TF-IDF] ➔ [RDBMS Warehouse]
Automated Scraping & Preprocessing: Dynamic streaming of Google Play Store reviews, handling text sanitization, deduplication, and ISO 8601 temporal data normalization.  Hybrid Sentiment Engine: Blends deep learning context-tracking via a DistilBERT Transformer (distilbert-base-uncased-finetuned-sst-2-english) with a rule-based VADER Lexicon for validation across short/noisy text arrays.  Thematic Classifier & TF-IDF Profile Mapping: Groups functional pain points into core operational matrices (e.g., Account Access, Transaction Performance, App Stability) while exposing unique cross-institutional term significance signals.  Database Engineering (3NF Warehouse): Relational schema architecture utilizing strict Third Normal Form constraints to link transactional multi-bank dimension registries with analytical reviews.📂 Project StructurePlaintext├── .github/workflows/    # CI/CD Automated Pipelines (GitHub Actions)
├── data/
│   └── processed/        # Cleaned metrics, analytical CSVs, and PNG charts
├── notebooks/            # Exploratory research and pipeline validations
├── scripts/              # RDBMS schemas and database ingestion utilities
├── src/                  # Core modules (preprocessing, NLP classification)
├── tests/                # Automated validation suites (PyTest)
├── requirements.txt      # Production runtime dependency map
└── README.md             # Project documentation
🚀 Quick Start & Installation1. PrerequisitesEnsure you have Python 3.11 installed on your system.2. Setup Environment & DependenciesBash# Clone the repository
git clone https://github.com/toleshee2015/fintech-review-analytics.git
cd fintech-review-analytics

# Create and activate a clean virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: .\venv\Scripts\activate

# Install requirements securely using an un-cached resolution process
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt --no-cache-dir
3. Initialize Database SchemaBash# Execute your 3NF database schema map
psql -U your_username -d your_database -f scripts/schema.sql
4. Run the Pipeline TestsBash# Run automated verification suites before staging updates
pytest --cov=src tests/
