"""
cashflow_kpis.py

Sprint 5
Cash Flow Intelligence

Outputs:
--------
output/cashflow_intelligence.xlsx
output/distress_alerts.csv
"""

from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "db" / "nifty100.db"

OUTPUT = BASE_DIR / "output"
OUTPUT.mkdir(exist_ok=True)


def load_data():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT

        fr.company_id,

        fr.year,

        fr.free_cash_flow_cr,

        fr.cash_from_operations_cr,

        fr.fcf_conversion_pct,

        fr.capital_allocation_pattern,

        fr.cfo_quality_score,

        fr.cfo_quality_label,

        fr.total_debt_cr,

        p.sales,

        p.net_profit,

        cf.operating_activity,

        cf.investing_activity,

        cf.financing_activity,

        bs.borrowings,

        s.broad_sector

    FROM financial_ratios fr

    LEFT JOIN profitandloss p
        ON fr.company_id=p.company_id
        AND fr.year=p.year

    LEFT JOIN cashflow cf
        ON fr.company_id=cf.company_id
        AND fr.year=cf.year

    LEFT JOIN balancesheet bs
        ON fr.company_id=bs.company_id
        AND fr.year=bs.year

    LEFT JOIN sectors s
        ON fr.company_id=s.company_id
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


def classify_capex(x):

    if pd.isna(x):
        return "Unknown"

    if x < 3:
        return "Asset Light"

    if x < 8:
        return "Moderate"

    return "Capital Intensive"


def build(df):

    df["capex_intensity_pct"] = (df["investing_activity"].abs() / df["sales"]) * 100

    df["capex_label"] = df["capex_intensity_pct"].apply(classify_capex)

    df["distress_flag"] = (df["operating_activity"] < 0) & (
        df["financing_activity"] > 0
    )

    df = df.sort_values(
        [
            "company_id",
            "year",
        ]
    )

    df["prev_debt"] = df.groupby("company_id")["borrowings"].shift(1)

    df["deleveraging_flag"] = (df["financing_activity"] < 0) & (
        df["borrowings"] < df["prev_debt"]
    )

    return df


def export(df):

    cols = [
        "company_id",
        "broad_sector",
        "cfo_quality_score",
        "cfo_quality_label",
        "capex_intensity_pct",
        "capex_label",
        "fcf_conversion_pct",
        "capital_allocation_pattern",
        "distress_flag",
        "deleveraging_flag",
    ]

    df[cols].to_excel(
        OUTPUT / "cashflow_intelligence.xlsx",
        index=False,
    )

    alerts = df[df["distress_flag"]]

    alerts.to_csv(
        OUTPUT / "distress_alerts.csv",
        index=False,
    )


def main():

    df = load_data()

    df = build(df)

    export(df)

    print("=" * 60)

    print("Cashflow Intelligence Complete")

    print("=" * 60)

    print(df.head())

    print()

    print("Rows :", len(df))


if __name__ == "__main__":
    main()
