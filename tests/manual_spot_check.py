import sqlite3

conn = sqlite3.connect("db/nifty100.db")
conn.row_factory = sqlite3.Row

companies = [
    "ABB",
    "TCS",
    "RELIANCE",
]

print("=" * 70)
print("SPRINT 2 MANUAL SPOT CHECK")
print("=" * 70)

for company in companies:
    print("\n", company)

    rows = conn.execute(
        """
        SELECT
            year,
            return_on_equity_pct,
            revenue_cagr_5yr
        FROM financial_ratios
        WHERE company_id=?
        ORDER BY year DESC
        LIMIT 5
        """,
        (company,),
    ).fetchall()

    for row in rows:
        print(
            row["year"],
            "ROE =",
            row["return_on_equity_pct"],
            "| Revenue CAGR =",
            row["revenue_cagr_5yr"],
        )

conn.close()
