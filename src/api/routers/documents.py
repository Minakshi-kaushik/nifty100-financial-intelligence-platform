"""
documents.py

Annual Report API
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
# DOCUMENTS
# =====================================================


@router.get("/companies/{ticker}/documents")
def company_documents(ticker: str):

    sql = """

    SELECT

        year,

        annual_report

    FROM documents

    WHERE company_id=?

    ORDER BY year DESC

    """

    df = query(sql, [ticker])

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail="Documents not found",
        )

    reports = []

    for _, row in df.iterrows():
        url = row["annual_report"]

        reports.append(
            {
                "year": row["year"],
                "annual_report": url,
                "is_url_valid": isinstance(url, str) and url.startswith("http"),
            }
        )

    return reports
