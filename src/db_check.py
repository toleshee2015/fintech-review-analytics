from src.database import get_connection

def check_connection():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT version();")
    print(cur.fetchone())

    cur.close()
    conn.close()

    print("Database connection OK")

if __name__ == "__main__":
    check_connection()
