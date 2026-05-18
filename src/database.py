from sqlalchemy import create_engine

def get_engine():
    return create_engine("postgresql://user:password@localhost:5432/bank_reviews")
