"""
health.py

Health endpoint.
"""

import time
from pathlib import Path
import sqlite3

from fastapi import APIRouter

router = APIRouter()

START_TIME = time.time()

BASE_DIR = Path(__file__).resolve().parents[3]
DB_PATH = BASE_DIR / "db" / "nifty100.db"


@router.get("/health")
def health():

    conn = sqlite3.connect(DB_PATH)

    cur = conn.cursor()

    tables = [
        "companies",
        "balancesheet",
        "cashflow",
        "profitandloss",
        "financial_ratios",
        "market_cap",
        "documents",
        "peer_groups",
        "stock_prices",
        "sectors",
    ]

    counts = {}

    for table in tables:
        try:
            cur.execute(f"SELECT COUNT(*) FROM {table}")

            counts[table] = cur.fetchone()[0]

        except Exception:
            counts[table] = 0

    conn.close()

    return {
        "status": "ok",
        "version": "1.0.0",
        "uptime_seconds": round(
            time.time() - START_TIME,
            2,
        ),
        "db_row_counts": counts,
    }
