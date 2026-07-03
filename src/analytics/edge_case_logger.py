"""
edge_case_logger.py

Creates ratio_edge_cases.log
"""

from pathlib import Path
import sqlite3

DB_PATH = Path("db") / "nifty100.db"

OUTPUT = Path("output") / "ratio_edge_cases.log"


def log(msg, f):
    f.write(msg + "\n")


def generate_log():

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute("SELECT * FROM financial_ratios")

    rows = cur.fetchall()

    OUTPUT.parent.mkdir(exist_ok=True)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        log("=" * 70, f)
        log("Ratio Edge Case Report", f)
        log("=" * 70, f)

        for row in rows:
            cid = row["company_id"]
            year = row["year"]

            if row["debt_to_equity"] == 0:
                log(f"{cid} {year} : Debt Free Company", f)

            if row["interest_coverage"] is None:
                log(f"{cid} {year} : Interest Coverage N/A", f)

            if row["return_on_equity_pct"] is None:
                log(f"{cid} {year} : Negative/Zero Equity", f)

            if row["revenue_cagr_flag"] != "NORMAL":
                log(
                    f"{cid} {year} : Revenue CAGR -> {row['revenue_cagr_flag']}",
                    f,
                )

            if row["pat_cagr_flag"] != "NORMAL":
                log(
                    f"{cid} {year} : PAT CAGR -> {row['pat_cagr_flag']}",
                    f,
                )

            if row["eps_cagr_flag"] != "NORMAL":
                log(
                    f"{cid} {year} : EPS CAGR -> {row['eps_cagr_flag']}",
                    f,
                )

    conn.close()

    print("=" * 60)
    print("Edge Case Log Generated")
    print("=" * 60)
    print(OUTPUT)


if __name__ == "__main__":
    generate_log()
