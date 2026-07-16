import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "db" / "nifty100.db"

print(BASE_DIR)
print(DB_PATH)


@st.cache_data(ttl=600)
def run_query(query, params=None):

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(
        query,
        conn,
        params=params,
    )

    conn.close()

    return df


# ==========================================================
# Companies
# ==========================================================


@st.cache_data(ttl=600)
def get_companies():

    query = """
    SELECT *
    FROM companies
    ORDER BY company_name
    """

    return run_query(query)


@st.cache_data(ttl=600)
def get_company(company):

    query = """
    SELECT *
    FROM companies
    WHERE id=?
    """

    return run_query(query, [company])


# ==========================================================
# Financial Ratios
# ==========================================================


@st.cache_data(ttl=600)
def get_ratios(company=None, year=None):

    query = """
    SELECT *
    FROM financial_ratios
    WHERE 1=1
    """

    params = []

    if company is not None:
        query += " AND company_id=?"
        params.append(company)

    if year is not None:
        query += " AND year=?"
        params.append(year)

    return run_query(query, params)


@st.cache_data(ttl=600)
def get_latest_ratios():

    query = """
    SELECT *
    FROM financial_ratios
    WHERE year='TTM'
    """

    return run_query(query)


# ==========================================================
# Profit & Loss
# ==========================================================


@st.cache_data(ttl=600)
def get_profit_loss(company):

    query = """
    SELECT *
    FROM profitandloss
    WHERE company_id=?
    """

    return run_query(query, [company])


# ==========================================================
# Balance Sheet
# ==========================================================


@st.cache_data(ttl=600)
def get_balance_sheet(company):

    query = """
    SELECT *
    FROM balancesheet
    WHERE company_id=?
    """

    return run_query(query, [company])


# ==========================================================
# Cash Flow
# ==========================================================


@st.cache_data(ttl=600)
def get_cashflow(company):

    query = """
    SELECT *
    FROM cashflow
    WHERE company_id=?
    """

    return run_query(query, [company])


# ==========================================================
# Sectors
# ==========================================================


@st.cache_data(ttl=600)
def get_sectors():

    query = """
    SELECT *
    FROM sectors
    ORDER BY broad_sector
    """

    return run_query(query)


# ==========================================================
# Peer Groups
# ==========================================================


@st.cache_data(ttl=600)
def get_peer_groups():

    query = """
    SELECT *
    FROM peer_groups
    """

    return run_query(query)


@st.cache_data(ttl=600)
def get_peer_group(group):

    query = """
    SELECT *
    FROM peer_groups
    WHERE peer_group_name=?
    """

    return run_query(query, [group])


# ==========================================================
# Valuation
# ==========================================================


@st.cache_data(ttl=600)
def get_valuation(company=None):

    query = """
    SELECT *
    FROM valuation
    WHERE 1=1
    """

    params = []

    if company is not None:
        query += " AND company_id=?"
        params.append(company)

    return run_query(query, params)
