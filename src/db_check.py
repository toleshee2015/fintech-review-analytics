<<<<<<< HEAD

from database import get_engine
import pandas as pd

def check_connection():
    engine = get_engine()

    with engine.connect() as conn:
        print("Connection OK")
        print(conn.execute("SELECT 1").fetchone())

if __name__ == "__main__":
    check_connection()
=======
from database import get_engine
from sqlalchemy import text

def check():
    engine = get_engine()

    try:
        with engine.connect() as conn:
            print("Database connection successful!")
            print(conn.execute(text("SELECT 1")).fetchone())

    except Exception as e:
        print("Database connection failed:")
        print(e)

if __name__ == "__main__":
    check()
>>>>>>> task-3
