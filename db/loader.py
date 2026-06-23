from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "db" / "nifty100.db"
DATA_DIR = BASE_DIR / "data" / "raw"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

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
    print(f"\n{'=' * 70}")
    print(f"Loading {table_name}")
    print(f"{'=' * 70}")

    df = pd.read_excel(file_path, header=header_row)

    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    print(f"Rows Found : {len(df)}")
    print(f"Columns    : {len(df.columns)}")

    df.to_sql(table_name, conn, if_exists="append", index=False)

    print(f"Loaded {len(df)} rows")

    return {"table_name": table_name, "rows_loaded": len(df), "rows_rejected": 0}


def main():

    print("\nStarting Full Data Load...\n")

    conn = sqlite3.connect(DB_PATH)

    load_audit = []

    for table_name, (file_name, header_row) in FILES.items():
        audit_row = load_table(conn, table_name, DATA_DIR / file_name, header_row)

        load_audit.append(audit_row)

    conn.commit()
    conn.close()

    audit_df = pd.DataFrame(load_audit)

    audit_file = OUTPUT_DIR / "load_audit.csv"

    audit_df.to_csv(audit_file, index=False)

    print("\n" + "=" * 70)
    print("LOAD COMPLETE")
    print("=" * 70)

    print(f"\nAudit File Created : {audit_file}")

    print("\nSummary")
    print(audit_df)

    print("\nAll tables loaded successfully.")


if __name__ == "__main__":
    main()
