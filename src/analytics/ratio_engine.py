"""
ratio_engine.py

Sprint 2

Reads financial statements from SQLite,
computes all KPIs,
writes them into financial_ratios.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

from src.analytics.ratios import calculate_ratios
from src.analytics.cashflow_kpis import calculate_cashflow_kpis


DB_PATH = Path("db") / "nifty100.db"


# ==========================================================
# Database
# ==========================================================


def get_connection():

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    return conn


FETCH_QUERY = """
SELECT

p.company_id,
p.year,

c.company_name,

s.broad_sector,

-- Profit & Loss

p.sales,
p.operating_profit,
p.other_income,
p.interest,
p.opm_percentage,
p.net_profit,
p.eps,
p.dividend_payout,

-- Balance Sheet

b.equity_capital,
b.reserves,
b.borrowings,
b.investments,
b.total_assets,

-- Cash Flow

cf.operating_activity,
cf.investing_activity,
cf.financing_activity

FROM profitandloss p

JOIN balancesheet b
ON p.company_id=b.company_id
AND p.year=b.year

JOIN cashflow cf
ON p.company_id=cf.company_id
AND p.year=cf.year

LEFT JOIN sectors s
ON p.company_id=s.company_id

LEFT JOIN companies c
ON p.company_id=c.id

ORDER BY
p.company_id,
p.year;
"""


def fetch_financial_data(conn):

    cursor = conn.cursor()

    cursor.execute(FETCH_QUERY)

    return cursor.fetchall()


def process_record(row):
    """
    Calculate all KPIs for one company-year.
    """

    profitability = calculate_ratios(
        company=row["company_name"],
        year=row["year"],
        sales=row["sales"],
        net_profit=row["net_profit"],
        operating_profit=row["operating_profit"],
        other_income=row["other_income"],
        interest=row["interest"],
        opm_percentage=row["opm_percentage"],
        equity_capital=row["equity_capital"],
        reserves=row["reserves"],
        borrowings=row["borrowings"],
        investments=row["investments"],
        total_assets=row["total_assets"],
        broad_sector=row["broad_sector"] or "",
    )

    cashflow = calculate_cashflow_kpis(
        operating_activity=row["operating_activity"],
        investing_activity=row["investing_activity"],
        financing_activity=row["financing_activity"],
        operating_profit=row["operating_profit"],
        sales=row["sales"],
        cfo_history=[row["operating_activity"]],
        pat_history=[row["net_profit"]],
    )

    result = {}

    result.update(profitability)
    result.update(cashflow)

    return result


def process_record(row):
    """
    Calculate all KPIs for one company-year.
    """

    profitability = calculate_ratios(
        company=row["company_name"],
        year=row["year"],
        sales=row["sales"],
        net_profit=row["net_profit"],
        operating_profit=row["operating_profit"],
        other_income=row["other_income"],
        interest=row["interest"],
        opm_percentage=row["opm_percentage"],
        equity_capital=row["equity_capital"],
        reserves=row["reserves"],
        borrowings=row["borrowings"],
        investments=row["investments"],
        total_assets=row["total_assets"],
        broad_sector=row["broad_sector"] or "",
    )

    print(
        row["company_id"],
        row["year"],
        row["operating_activity"],
        row["investing_activity"],
    )

    cashflow = calculate_cashflow_kpis(
        operating_activity=row["operating_activity"] or 0,
        investing_activity=row["investing_activity"] or 0,
        financing_activity=row["financing_activity"] or 0,
        operating_profit=row["operating_profit"] or 0,
        sales=row["sales"] or 0,
        cfo_history=[row["operating_activity"] or 0],
        pat_history=[row["net_profit"] or 0],
    )
    result = {}

    result.update(profitability)
    result.update(cashflow)

    return result


def insert_financial_ratio(conn, row, ratios):
    """
    Insert one computed company-year record into financial_ratios.
    """

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO financial_ratios (

            company_id,
            year,

            net_profit_margin_pct,
            operating_profit_margin_pct,
            return_on_equity_pct,
            return_on_capital_employed_pct,
            return_on_assets_pct,

            debt_to_equity,
            interest_coverage,
            asset_turnover,
            net_debt_cr,

            high_leverage_flag,
            icr_warning_flag,
            icr_label,

            free_cash_flow_cr,
            capex_cr,
            fcf_conversion_pct,
            cash_from_operations_cr,
            cfo_quality_score,
            cfo_quality_label,
            capital_allocation_pattern,

            earnings_per_share,
            book_value_per_share,
            dividend_payout_ratio_pct,
            total_debt_cr,

            revenue_cagr_3yr,
            revenue_cagr_5yr,
            revenue_cagr_10yr,

            pat_cagr_3yr,
            pat_cagr_5yr,
            pat_cagr_10yr,

            eps_cagr_3yr,
            eps_cagr_5yr,
            eps_cagr_10yr,

            revenue_cagr_flag,
            pat_cagr_flag,
            eps_cagr_flag,

            composite_quality_score

        )
        VALUES (

            ?, ?,

            ?, ?, ?, ?, ?,

            ?, ?, ?, ?,

            ?, ?, ?,

            ?, ?, ?, ?, ?, ?,
            ?,

            ?, ?, ?, ?,

            ?, ?, ?,

            ?, ?, ?,

            ?, ?, ? ,

            ?, ?, ?,

            ?

        )
        """,
        (
            row["company_id"],
            row["year"],
            ratios.get("net_profit_margin_pct"),
            ratios.get("operating_profit_margin_pct"),
            ratios.get("return_on_equity_pct"),
            ratios.get("return_on_capital_employed_pct"),
            ratios.get("return_on_assets_pct"),
            ratios.get("debt_to_equity"),
            ratios.get("interest_coverage"),
            ratios.get("asset_turnover"),
            ratios.get("net_debt"),
            int(ratios.get("high_leverage_flag", False)),
            int(ratios.get("icr_warning_flag", False)),
            ratios.get("icr_label"),
            ratios.get("free_cash_flow_cr"),
            ratios.get("capex_cr"),
            ratios.get("fcf_conversion_pct"),
            row["operating_activity"],
            ratios.get("cfo_quality_score"),
            ratios.get("cfo_quality_label"),
            ratios.get("capital_allocation_pattern"),
            row["eps"],
            (
                (row["equity_capital"] + row["reserves"]) / row["equity_capital"]
                if row["equity_capital"] > 0
                else None
            ),
            row["dividend_payout"],
            row["borrowings"],
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ),
    )


if __name__ == "__main__":
    conn = get_connection()

    rows = fetch_financial_data(conn)

    # Get cursor
    cursor = conn.cursor()

    # Clear old computed ratios
    cursor.execute("DELETE FROM financial_ratios")

    inserted = 0

    for row in rows:
        ratios = process_record(row)

        insert_financial_ratio(conn, row, ratios)

        inserted += 1

    conn.commit()

    print("\n===================================")
    print(" Financial Ratio Engine")
    print("===================================")
    print(f"Rows Processed : {len(rows)}")
    print(f"Rows Inserted  : {inserted}")
    print("===================================")

    conn.close()
