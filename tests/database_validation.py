import sqlite3

conn = sqlite3.connect("db/nifty100.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM financial_ratios")
print(cursor.fetchone()[0])

cursor.execute("""
SELECT COUNT(*)
FROM financial_ratios
WHERE
    net_profit_margin_pct IS NOT NULL
""")
print(cursor.fetchone()[0])

conn.close()
