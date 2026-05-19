
from database import get_engine
import pandas as pd

def check_connection():
    engine = get_engine()

    with engine.connect() as conn:
        print("Connection OK")
        print(conn.execute("SELECT 1").fetchone())

if __name__ == "__main__":
    check_connection()
