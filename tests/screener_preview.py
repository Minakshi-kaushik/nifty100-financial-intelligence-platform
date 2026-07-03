import sqlite3

conn = sqlite3.connect("db/nifty100.db")
conn.row_factory = sqlite3.Row

rows = conn.execute(
    """
    SELECT

    company_id,
    year,
    return_on_equity_pct,
    debt_to_equity

    FROM financial_ratios

    WHERE
        return_on_equity_pct > 15
        AND debt_to_equity < 1

    ORDER BY
        return_on_equity_pct DESC
    """
).fetchall()

print("=" * 70)
print("SPRINT 2 SCREENER")
print("=" * 70)

print("Companies Found :", len(rows))
print()

for row in rows[:30]:
    print(
        f"{row['company_id']:15}"
        f"{row['year']:10}"
        f" ROE={row['return_on_equity_pct']:6}"
        f" D/E={row['debt_to_equity']}"
    )

conn.close()
