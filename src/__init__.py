from database import get_connection

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    with open("schema.sql", "r", encoding="utf-8") as file:
        sql = file.read()
        cur.execute(sql)

    conn.commit()
    cur.close()
    conn.close()
    print("Database schema created successfully.")

if __name__ == "__main__":
    create_tables()
