"""
valuation.py

Valuation API
"""

from pathlib import Path
import sqlite3

import pandas as pd

from fastapi import APIRouter, HTTPException

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
# MARKET CAP HISTORY
# =====================================================


@router.get("/market-cap/{ticker}")
def market_cap_history(ticker: str):

    sql = """

    SELECT

        year,

        market_cap_crore,

        enterprise_value_crore,

        pe_ratio,

        pb_ratio,

        ev_ebitda,

        dividend_yield_pct

    FROM market_cap

    WHERE company_id=?

    ORDER BY year

    """

    df = query(sql, [ticker])

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail="Company not found",
        )

    return df.to_dict(orient="records")
