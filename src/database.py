import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "database": "bank_reviews",
    "user": "postgres",
    "password": "123",
    "port": 5432
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)
