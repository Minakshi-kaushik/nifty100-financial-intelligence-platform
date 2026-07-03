import sqlite3

conn = sqlite3.connect("db/nifty100.db")
conn.row_factory = sqlite3.Row

cursor = conn.cursor()

cursor.execute("""
SELECT
    p.company_id,
    p.year,
    COUNT(*) AS cnt
FROM profitandloss p

JOIN balancesheet b
ON p.company_id = b.company_id
AND p.year = b.year

LEFT JOIN cashflow cf
ON p.company_id = cf.company_id
AND p.year = cf.year

LEFT JOIN sectors s
ON p.company_id = s.company_id

GROUP BY p.company_id, p.year
HAVING cnt > 1
ORDER BY cnt DESC
""")

rows = cursor.fetchall()

print(f"Duplicate company-years: {len(rows)}\n")

for row in rows[:30]:
    print(dict(row))

conn.close()
