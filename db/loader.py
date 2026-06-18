import sqlite3
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "db" / "nifty100.db"

DATA_DIR = BASE_DIR / "data" / "raw"

FILES = {
    "companies": ("companies.xlsx", 1),
    "market_cap": ("market_cap.xlsx", 0),
    "peer_groups": ("peer_groups.xlsx", 0),
    "sectors": ("sectors.xlsx", 0),
    "stock_prices": ("stock_prices.xlsx", 0),
    "financial_ratios": ("financial_ratios.xlsx", 0),
    "analysis": ("analysis.xlsx", 1),
    "balancesheet": ("balancesheet.xlsx", 1),
    "cashflow": ("cashflow.xlsx", 1),
    "documents": ("documents.xlsx", 1),
    "profitandloss": ("profitandloss.xlsx", 1),
    "prosandcons": ("prosandcons.xlsx", 1),
}


def load_table(conn, table_name, file_path, header_row):

    print(f"\nLoading {table_name}...")
    print(f"Reading: {file_path}")

    df = pd.read_excel(file_path, header=header_row)

    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    print("Columns:")
    print(df.columns.tolist())

    df.to_sql(table_name, conn, if_exists="replace", index=False)

    print(f"Loaded {len(df)} rows")


def main():

    conn = sqlite3.connect(DB_PATH)

    for table, (file_name, header_row) in FILES.items():
        load_table(conn, table, DATA_DIR / file_name, header_row)

    conn.commit()
    conn.close()

    print("\nAll tables loaded successfully.")


if __name__ == "__main__":
    main()
