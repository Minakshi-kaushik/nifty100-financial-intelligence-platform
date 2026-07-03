import sqlite3
from pathlib import Path


DB_PATH = Path("db") / "nifty100.db"


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    print("=" * 60)
    print("RATIO ENGINE VALIDATION")
    print("=" * 60)

    # ---------------------------------------------------
    # Total Rows
    # ---------------------------------------------------

    cursor.execute("""
    SELECT COUNT(*)
    FROM financial_ratios
    """)

    rows = cursor.fetchone()[0]

    print(f"\nTotal Financial Ratio Rows : {rows}")

    # ---------------------------------------------------
    # Duplicate Records
    # ---------------------------------------------------

    cursor.execute("""
    SELECT company_id,
           year,
           COUNT(*) as cnt
    FROM financial_ratios
    GROUP BY company_id, year
    HAVING cnt > 1
    """)

    duplicates = cursor.fetchall()

    print(f"Duplicate Records : {len(duplicates)}")

    # ---------------------------------------------------
    # NULL Count Check
    # ---------------------------------------------------

    cursor.execute("""
    SELECT

    COUNT(net_profit_margin_pct),
    COUNT(operating_profit_margin_pct),
    COUNT(return_on_equity_pct),
    COUNT(return_on_capital_employed_pct),
    COUNT(return_on_assets_pct),

    COUNT(debt_to_equity),
    COUNT(interest_coverage),
    COUNT(asset_turnover),

    COUNT(free_cash_flow_cr),
    COUNT(capex_cr),

    COUNT(revenue_cagr_5yr)

    FROM financial_ratios
    """)

    counts = cursor.fetchone()

    labels = [
        "Net Profit Margin",
        "Operating Margin",
        "ROE",
        "ROCE",
        "ROA",
        "Debt/Equity",
        "Interest Coverage",
        "Asset Turnover",
        "Free Cash Flow",
        "CapEx",
        "Revenue CAGR 5Y",
    ]

    print("\nPopulated Values\n")

    for label, value in zip(labels, counts):
        print(f"{label:30} : {value}")

    # ---------------------------------------------------
    # Sample Records
    # ---------------------------------------------------

    cursor.execute("""
    SELECT *
    FROM financial_ratios
    LIMIT 5
    """)

    print("\nSample Records\n")

    for row in cursor.fetchall():
        print(dict(row))
        print("-" * 60)

    conn.close()


if __name__ == "__main__":
    main()
