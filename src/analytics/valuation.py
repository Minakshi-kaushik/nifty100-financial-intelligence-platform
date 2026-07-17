"""
valuation.py
Skeleton compatible with user's schema.
Replace/extend logic as needed.
"""

from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "db" / "nifty100.db"
OUT = BASE_DIR / "output"
OUT.mkdir(exist_ok=True)


def load_data():
    conn = sqlite3.connect(DB_PATH)
    query = """
    WITH latest_ratios AS (
      SELECT * FROM financial_ratios
      WHERE year = 'Mar 2024'
    ),
    latest_market AS (
      SELECT * FROM market_cap
      WHERE year= 2024
    )
    SELECT
      fr.company_id,
      c.company_name,
      s.broad_sector,
      fr.free_cash_flow_cr,
      mc.market_cap_crore,
      mc.pe_ratio,
      mc.pb_ratio,
      mc.ev_ebitda
    FROM latest_ratios fr
    LEFT JOIN companies c ON c.id=fr.company_id
    LEFT JOIN sectors s ON s.company_id=fr.company_id
    LEFT JOIN latest_market mc ON mc.company_id=fr.company_id;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    print(df.shape)
    print(df.head())
    return df


def build(df):
    df["fcf_yield_pct"] = (df["free_cash_flow_cr"] / df["market_cap_crore"]) * 100
    med = df.groupby("broad_sector")["pe_ratio"].median().rename("sector_median_pe")
    df = df.merge(med, on="broad_sector")
    df["pe_vs_sector_median_pct"] = df["pe_ratio"] / df["sector_median_pe"] * 100

    def flag(r):
        if pd.isna(r.pe_ratio):
            return "N/A"
        if r.pe_ratio > 1.5 * r.sector_median_pe:
            return "Caution"
        if r.pe_ratio < 0.7 * r.sector_median_pe:
            return "Discount"
        return "Fair"

    df["flag"] = df.apply(flag, axis=1)
    return df


def export(df):
    cols = [
        "company_id",
        "company_name",
        "broad_sector",
        "pe_ratio",
        "pb_ratio",
        "ev_ebitda",
        "fcf_yield_pct",
        "sector_median_pe",
        "pe_vs_sector_median_pct",
        "flag",
    ]
    df[cols].to_excel(OUT / "valuation_summary.xlsx", index=False)
    df[df["flag"].isin(["Caution", "Discount"])][cols].to_csv(
        OUT / "valuation_flags.csv", index=False
    )


if __name__ == "__main__":
    d = build(load_data())
    export(d)
    print("Done", len(d))
