from src.database import get_engine
import pandas as pd

def check_connection():
    engine = get_engine()

    try:
        with engine.connect() as conn:
            print("Database connection successful!")
            result = conn.execute("SELECT 1")
            print(result.fetchone())

    except Exception as e:
        print("Database connection failed:")
        print(e)

def preview_data():
    engine = get_engine()

    try:
        df = pd.read_sql("SELECT * FROM reviews LIMIT 5", engine)
        print(df)

    except Exception as e:
        print("Failed to fetch data:")
        print(e)

if __name__ == "__main__":
    check_connection()
    preview_data()
