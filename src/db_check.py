from sqlalchemy import text
from src.database import get_engine

def check_db():
    engine = get_engine()

    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM reviews"))
        print("Total reviews:", result.fetchone()[0])

if __name__ == "__main__":
    check_db()
