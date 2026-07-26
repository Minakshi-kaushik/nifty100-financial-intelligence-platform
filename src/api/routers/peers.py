"""
peers.py

Peer Group API
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
# PEER GROUP
# =====================================================


@router.get("/peers/{group_name}")
def peer_group(group_name: str):

    sql = """

    SELECT

        pp.company_id,

        c.company_name,

        pp.metric,

        pp.value,

        pp.percentile_rank

    FROM peer_percentiles pp

    JOIN companies c

        ON pp.company_id=c.id

    WHERE

        pp.peer_group_name=?

    ORDER BY

        pp.company_id

    """

    df = query(sql, [group_name])

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail="Peer group not found",
        )

    return df.to_dict(orient="records")


# =====================================================
# COMPANY VS PEERS
# =====================================================


@router.get("/companies/{ticker}/peers/compare")
def compare_peers(ticker: str):

    sql = """

    SELECT

        metric,

        value,

        percentile_rank

    FROM peer_percentiles

    WHERE company_id=?

    """

    company = query(sql, [ticker])

    if company.empty:
        raise HTTPException(
            status_code=404,
            detail="Company not found",
        )

    sql = """

    SELECT

        peer_group_name

    FROM peer_groups

    WHERE company_id=?

    LIMIT 1

    """

    peer = query(sql, [ticker])

    if peer.empty:
        return {"company": company.to_dict(orient="records"), "peer_average": []}

    group = peer.iloc[0]["peer_group_name"]

    sql = """

    SELECT

        metric,

        AVG(value) AS average_value

    FROM peer_percentiles

    WHERE peer_group_name=?

    GROUP BY metric

    """

    avg = query(sql, [group])

    return {
        "company": company.to_dict(orient="records"),
        "peer_average": avg.to_dict(orient="records"),
        "peer_group": group,
    }
