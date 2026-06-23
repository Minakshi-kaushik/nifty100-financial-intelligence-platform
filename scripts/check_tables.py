# scripts/check_tables.py

import sqlite3

conn = sqlite3.connect("db/nifty100.db")

tables = conn.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
ORDER BY name
""").fetchall()

for t in tables:
    print(t[0])

conn.close()
