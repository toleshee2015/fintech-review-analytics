
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

);

    review_date DATE,

    sentiment_label VARCHAR(20),
    sentiment_score NUMERIC(5,4),
    identified_theme VARCHAR(100),
    language VARCHAR(10),

    CONSTRAINT fk_bank
        FOREIGN KEY (bank_id)
        REFERENCES banks(bank_id)
        ON DELETE CASCADE
);


-- BANKS TABLE

CREATE TABLE IF NOT EXISTS banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) UNIQUE NOT NULL
);


-- REVIEWS TABLE

CREATE TABLE IF NOT EXISTS reviews (
    review_id SERIAL PRIMARY KEY,
    bank_id INTEGER NOT NULL,
    review_text TEXT NOT NULL,
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    review_date DATE,

    sentiment_label VARCHAR(20),
    sentiment_score NUMERIC(5,4),
    identified_theme VARCHAR(100),
    language VARCHAR(10),

    CONSTRAINT fk_bank
        FOREIGN KEY (bank_id)
        REFERENCES banks(bank_id)
        ON DELETE CASCADE
);

