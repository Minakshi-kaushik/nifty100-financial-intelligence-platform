import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DB_PATH = BASE_DIR / "nifty100.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"


def create_database():
    print("Creating database...")

    conn = sqlite3.connect(DB_PATH)

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    conn.executescript(schema_sql)

    conn.commit()
    conn.close()

    print(f"Database created successfully: {DB_PATH}")


if __name__ == "__main__":
    create_database()
