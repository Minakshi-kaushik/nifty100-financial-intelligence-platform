import sqlite3
from pathlib import Path

DB_PATH = Path("db") / "nifty100.db"

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row

cursor = conn.cursor()

company = "TCS"  # Change to any company_id

cursor.execute(
    """
SELECT *

FROM financial_ratios

WHERE company_id=?

ORDER BY year
""",
    (company,),
)

rows = cursor.fetchall()

print(f"\n{company}\n")

for row in rows:
    print(
        row["year"],
        row["return_on_equity_pct"],
        row["debt_to_equity"],
        row["interest_coverage"],
        row["free_cash_flow_cr"],
        row["revenue_cagr_5yr"],
    )

conn.close()
