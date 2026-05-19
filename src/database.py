from sqlalchemy import create_engine

def get_engine():
    return create_engine(
        "postgresql+psycopg2://postgres:123@localhost:5432/fintech_reviews"
    )
