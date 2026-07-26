"""
screener.py

Company Screener API
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


@router.get("/screener")
def screener(
    min_roe: float | None = None,
    max_de: float | None = None,
    min_fcf: float | None = None,
    sector: str | None = None,
    min_rev_cagr_5yr: float | None = None,
    min_pat_cagr_5yr: float | None = None,
    max_pe: float | None = None,
):

    sql = """
    SELECT

        fr.company_id,

        c.company_name,

        s.broad_sector,

        fr.return_on_equity_pct,

        fr.debt_to_equity,

        fr.free_cash_flow_cr,

        fr.revenue_cagr_5yr,

        fr.pat_cagr_5yr,

        mc.pe_ratio

    FROM financial_ratios fr

    JOIN companies c

        ON fr.company_id=c.id

    LEFT JOIN sectors s

        ON fr.company_id=s.company_id

    LEFT JOIN market_cap mc

        ON fr.company_id=mc.company_id

    WHERE

        fr.year='Mar 2024'

        AND mc.year=2024
    """

    params = []

    if min_roe is not None:
        sql += " AND fr.return_on_equity_pct>=?"

        params.append(min_roe)

    if max_de is not None:
        sql += " AND fr.debt_to_equity<=?"

        params.append(max_de)

    if min_fcf is not None:
        sql += " AND fr.free_cash_flow_cr>=?"

        params.append(min_fcf)

    if sector:
        sql += " AND s.broad_sector=?"

        params.append(sector)

    if min_rev_cagr_5yr is not None:
        sql += " AND fr.revenue_cagr_5yr>=?"

        params.append(min_rev_cagr_5yr)

    if min_pat_cagr_5yr is not None:
        sql += " AND fr.pat_cagr_5yr>=?"

        params.append(min_pat_cagr_5yr)

    if max_pe is not None:
        sql += " AND mc.pe_ratio<=?"

        params.append(max_pe)

    sql += """

    ORDER BY

        fr.return_on_equity_pct DESC
    """

    df = query(sql, params)

    return df.to_dict(orient="records")


@router.get("/screener/presets/quality")
def quality():

    sql = """

    SELECT

        company_id,

        return_on_equity_pct,

        debt_to_equity,

        free_cash_flow_cr,

        composite_quality_score

    FROM financial_ratios

    WHERE

        year='Mar 2024'

        AND return_on_equity_pct>=15

        AND debt_to_equity<=1

        AND free_cash_flow_cr>0

    ORDER BY

        composite_quality_score DESC

    """

    df = query(sql)

    return df.to_dict(orient="records")
