"""
portfolio.py

Portfolio Statistics API
"""

from pathlib import Path
import sqlite3

import pandas as pd

from fastapi import APIRouter

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parents[3]

DB_PATH = BASE_DIR / "db" / "nifty100.db"


def query(sql, params=None):

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(
        sql,
        conn,
        params=params,
    )

    conn.close()

    return df


# =====================================================
# PORTFOLIO STATISTICS
# =====================================================


@router.get("/portfolio/stats")
def portfolio_stats():

    sql = """

    SELECT *

    FROM financial_ratios

    WHERE year='Mar 2024'

    """

    df = query(sql)

    if df.empty:
        return []

    metrics = [
        "return_on_equity_pct",
        "return_on_capital_employed_pct",
        "return_on_assets_pct",
        "debt_to_equity",
        "free_cash_flow_cr",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "eps_cagr_5yr",
        "earnings_per_share",
        "book_value_per_share",
    ]

    output = []

    for metric in metrics:
        if metric not in df.columns:
            continue

        s = df[metric].dropna()

        output.append(
            {
                "metric": metric,
                "P10": round(s.quantile(0.10), 2),
                "P25": round(s.quantile(0.25), 2),
                "P50": round(s.quantile(0.50), 2),
                "P75": round(s.quantile(0.75), 2),
                "P90": round(s.quantile(0.90), 2),
                "Mean": round(s.mean(), 2),
                "Std": round(s.std(), 2),
            }
        )

    return output
