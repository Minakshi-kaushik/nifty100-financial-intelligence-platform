import sqlite3

conn = sqlite3.connect("db/nifty100.db")
cur = conn.cursor()

cur.execute("PRAGMA table_info(financial_ratios)")

for col in cur.fetchall():
    print(col[1])

conn.close()
