"""
capital_allocation_export.py

Exports capital allocation patterns for every company-year.

Output:
output/capital_allocation.csv
"""

from pathlib import Path
import sqlite3
import pandas as pd

DB_PATH = Path("db") / "nifty100.db"
OUTPUT_PATH = Path("output") / "capital_allocation.csv"


def export_capital_allocation():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT

        company_id,
        year,

        CASE
            WHEN cash_from_operations_cr >= 0
            THEN '+'
            ELSE '-'
        END AS cfo_sign,

        CASE
            WHEN free_cash_flow_cr >= cash_from_operations_cr
            THEN '+'
            ELSE '-'
        END AS cfi_sign,

        CASE
            WHEN net_debt_cr > 0
            THEN '+'
            ELSE '-'
        END AS cff_sign,

        capital_allocation_pattern

    FROM financial_ratios

    ORDER BY company_id, year
    """

    df = pd.read_sql_query(query, conn)

    OUTPUT_PATH.parent.mkdir(exist_ok=True)

    df.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    conn.close()

    print("=" * 60)
    print("Capital Allocation Export Complete")
    print("=" * 60)
    print(df.head())
    print(f"\nSaved to {OUTPUT_PATH}")


if __name__ == "__main__":
    export_capital_allocation()
