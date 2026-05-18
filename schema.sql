CREATE TABLE banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    bank_id INTEGER REFERENCES banks(bank_id),
    review_text TEXT NOT NULL,
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    sentiment_label VARCHAR(20),
    sentiment_score NUMERIC,
    identified_theme VARCHAR(100)
);
