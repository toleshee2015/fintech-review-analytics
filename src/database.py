from sqlalchemy import create_engine
from sqlalchemy import text
from src. database import get_engine

def check_db():
    engine = get_engine()

    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT COUNT(*) FROM reviews")
        )

        print(result.fetchone())

if __name__ == "__main__":
    check_db()
def get_engine():
    return create_engine("postgresql://user:password@localhost:5432/bank_reviews")
