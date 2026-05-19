CREATE TABLE banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100),
    app_name VARCHAR(100)
);

CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    bank_id INT REFERENCES banks(bank_id),
    review_text TEXT,
    rating INT,
    review_date DATE,
    sentiment_label VARCHAR(20),
    sentiment_score FLOAT,
    identified_theme VARCHAR(50),
    source VARCHAR(50)

      CONSTRAINT fk_bank
        FOREIGN KEY (bank_id)
        REFERENCES banks(bank_id)
        ON DELETE CASCADE
);
