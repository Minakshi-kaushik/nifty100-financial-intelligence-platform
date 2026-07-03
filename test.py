import sqlite3

conn = sqlite3.connect("db/nifty100.db")
cursor = conn.cursor()

cursor.execute("""
SELECT COUNT(*)
FROM profitandloss
""")
print("Profit rows:", cursor.fetchone()[0])

cursor.execute("""
SELECT COUNT(*)
FROM balancesheet
""")
print("Balance rows:", cursor.fetchone()[0])

cursor.execute("""
SELECT COUNT(*)
FROM cashflow
""")
print("Cashflow rows:", cursor.fetchone()[0])

conn.close()
