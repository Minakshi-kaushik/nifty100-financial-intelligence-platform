# scripts/create_db.py

import sqlite3
from pathlib import Path

DB_PATH = "db/nifty100.db"
SCHEMA_PATH = "db/schema.sql"

conn = sqlite3.connect(DB_PATH)

with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    conn.executescript(f.read())

conn.commit()
conn.close()

print("Database created successfully.")
