"""
sectors.py

Sector API
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
# ALL SECTORS
# =====================================================


@router.get("/sectors")
def all_sectors():

    sql = """

    SELECT

        s.broad_sector,

        COUNT(DISTINCT s.company_id) AS company_count,

        ROUND(
            AVG(fr.return_on_equity_pct),
            2
        ) AS median_roe,

        ROUND(
            AVG(mc.pe_ratio),
            2
        ) AS median_pe,

        ROUND(
            AVG(fr.debt_to_equity),
            2
        ) AS median_de

    FROM sectors s

    LEFT JOIN financial_ratios fr

        ON s.company_id=fr.company_id

    LEFT JOIN market_cap mc

        ON s.company_id=mc.company_id

    WHERE

        fr.year='Mar 2024'

        AND mc.year=2024

    GROUP BY

        s.broad_sector

    ORDER BY

        s.broad_sector

    """

    df = query(sql)
    df = df.astype(object)
    df = df.where(pd.notnull(df), None)

    return df.to_dict(orient="records")


# =====================================================
# COMPANIES IN A SECTOR
# =====================================================


@router.get("/sectors/{sector}/companies")
def sector_companies(sector: str):

    sql = """

    SELECT

        c.id,

        c.company_name,

        s.broad_sector,

        fr.return_on_equity_pct,

        fr.debt_to_equity,

        fr.free_cash_flow_cr,

        fr.composite_quality_score

    FROM companies c

    JOIN sectors s

        ON c.id=s.company_id

    JOIN financial_ratios fr

        ON c.id=fr.company_id

    WHERE

        s.broad_sector=?

        AND fr.year='Mar 2024'

    ORDER BY

        c.company_name

    """

    df = query(sql, [sector])

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail="Sector not found",
        )

    df = df.astype(object)
    df = df.where(pd.notnull(df), None)

    return df.to_dict(orient="records")
