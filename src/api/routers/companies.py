"""
companies.py

Company endpoints.
"""

import sqlite3
from pathlib import Path

import pandas as pd

from fastapi import APIRouter, HTTPException

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parents[3]

DB_PATH = BASE_DIR / "db" / "nifty100.db"
print("API DB:", DB_PATH.resolve())


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
# GET ALL COMPANIES
# =====================================================


@router.get("/companies")
def get_companies(
    sector: str | None = None,
    market_cap_category: str | None = None,
    search: str | None = None,
):

    sql = """
    SELECT

        c.id,

        c.company_name,

        s.broad_sector,

        s.sub_sector,

        s.market_cap_category,

        c.roe_percentage,

        c.roce_percentage

    FROM companies c

    LEFT JOIN sectors s

        ON c.id=s.company_id

    WHERE 1=1
    """

    params = []

    if sector:
        sql += " AND s.broad_sector=?"

        params.append(sector)

    if market_cap_category:
        sql += " AND s.market_cap_category=?"

        params.append(market_cap_category)

    if search:
        sql += """
        AND
        (
            c.company_name LIKE ?
            OR c.id LIKE ?
        )
        """

        params.append(f"%{search}%")

        params.append(f"%{search}%")

    sql += " ORDER BY c.company_name"

    df = query(sql, params)

    df = df.astype(object)
    df = df.where(pd.notnull(df), None)

    return df.to_dict(orient="records")


# =====================================================
# COMPANY PROFILE
# =====================================================


@router.get("/companies/{ticker}")
def company_profile(ticker: str):

    sql = """
    SELECT

        c.*,

        s.*,

        fr.*

    FROM companies c

    LEFT JOIN sectors s

        ON c.id=s.company_id

    LEFT JOIN financial_ratios fr

        ON c.id=fr.company_id

    WHERE

        c.id=?

        AND fr.year='Mar 2024'
    """

    df = query(sql, [ticker])

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail="Company not found",
        )

    df = df.astype(object)
    df = df.where(pd.notnull(df), None)

    return df.iloc[0].to_dict()


# =====================================================
# HISTORY HELPER
# =====================================================


def history(table, ticker, from_year=None, to_year=None):

    sql = f"""

    SELECT *

    FROM {table}

    WHERE company_id=?

    """

    params = [ticker]

    if from_year:
        sql += " AND year>=?"

        params.append(from_year)

    if to_year:
        sql += " AND year<=?"

        params.append(to_year)

    sql += " ORDER BY year"

    return query(sql, params)


# =====================================================
# PROFIT & LOSS
# =====================================================


@router.get("/companies/{ticker}/pl")
def profit_loss(
    ticker: str,
    from_year: str | None = None,
    to_year: str | None = None,
):

    df = history(
        "profitandloss",
        ticker,
        from_year,
        to_year,
    )
    df = df.astype(object)
    df = df.where(pd.notnull(df), None)
    return df.to_dict(orient="records")


# =====================================================
# BALANCE SHEET
# =====================================================


@router.get("/companies/{ticker}/bs")
def balance_sheet(
    ticker: str,
    from_year: str | None = None,
    to_year: str | None = None,
):

    df = history(
        "balancesheet",
        ticker,
        from_year,
        to_year,
    )
    df = df.astype(object)
    df = df.where(pd.notnull(df), None)

    return df.to_dict(orient="records")


# =====================================================
# CASHFLOW
# =====================================================


@router.get("/companies/{ticker}/cashflow")
def cashflow(
    ticker: str,
    from_year: str | None = None,
    to_year: str | None = None,
):

    df = history(
        "cashflow",
        ticker,
        from_year,
        to_year,
    )

    df = df.astype(object)
    df = df.where(pd.notnull(df), None)
    return df.to_dict(orient="records")


# =====================================================
# RATIOS
# =====================================================


@router.get("/companies/{ticker}/ratios")
def ratios(
    ticker: str,
    year: str | None = None,
):

    sql = """

    SELECT *

    FROM financial_ratios

    WHERE company_id=?

    """

    params = [ticker]

    if year:
        sql += " AND year=?"

        params.append(year)

    sql += " ORDER BY year"

    df = query(sql, params)

    df = df.astype(object)
    df = df.where(pd.notnull(df), None)

    return df.to_dict(orient="records")


# =====================================================
# TEARSHEET PDF
# =====================================================

from fastapi.responses import FileResponse

TEARSHEET_DIR = BASE_DIR / "reports" / "tearsheets"


@router.get("/companies/{ticker}/tearsheet")
def tearsheet(ticker: str):

    pdf = TEARSHEET_DIR / f"{ticker}_tearsheet.pdf"

    if not pdf.exists():
        raise HTTPException(
            status_code=404,
            detail="Tearsheet not found",
        )

    return FileResponse(
        path=str(pdf),
        filename=pdf.name,
        media_type="application/pdf",
    )
