import sqlite3

conn = sqlite3.connect("db/nifty100.db")
cursor = conn.cursor()

tables = [
    ("profitandloss", True),
    ("balancesheet", True),
    ("cashflow", True),
    ("sectors", False),
]

for table, has_year in tables:
    print(f"\n{'=' * 60}")
    print(table.upper())
    print("=" * 60)

    if has_year:
        cursor.execute(f"""
        SELECT company_id, year, COUNT(*)
        FROM {table}
        GROUP BY company_id, year
        HAVING COUNT(*) > 1
        ORDER BY COUNT(*) DESC
        """)
    else:
        cursor.execute(f"""
        SELECT company_id, COUNT(*)
        FROM {table}
        GROUP BY company_id
        HAVING COUNT(*) > 1
        ORDER BY COUNT(*) DESC
        """)

    rows = cursor.fetchall()

    if not rows:
        print("No duplicates")
    else:
        for row in rows:
            print(row)

conn.close()
