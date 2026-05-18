(
echo from sqlalchemy import text
echo from src.database import get_engine
echo.
echo def check_db():
echo     engine = get_engine()
echo.
echo     with engine.connect() as conn:
echo         result = conn.execute(text("SELECT COUNT(*) FROM reviews"))
echo         print(result.fetchone())
echo.
echo if __name__ == "__main__":
echo     check_db()
) > src\db_check.py
