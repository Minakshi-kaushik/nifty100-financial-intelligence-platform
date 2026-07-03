"""
ratio_engine.py

Sprint 2
Financial Ratio Engine
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

from src.analytics.ratios import calculate_ratios
from src.analytics.cashflow_kpis import calculate_cashflow_kpis
from src.analytics.cagr import calculate_metric_cagr

import csv

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


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
ON p.company_id = b.company_id
AND p.year = b.year

LEFT JOIN cashflow cf
ON p.company_id = cf.company_id
AND p.year = cf.year

LEFT JOIN sectors s
ON p.company_id = s.company_id

LEFT JOIN companies c
ON p.company_id = c.id

ORDER BY
p.company_id,
p.year;
"""


def fetch_financial_data(conn):

    cursor = conn.cursor()

    cursor.execute(FETCH_QUERY)

    return cursor.fetchall()


def load_company_history(conn, company_id):
    """
    Returns complete history of a company ordered oldest->latest.
    """

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT

        year,
        sales,
        net_profit,
        eps

        FROM profitandloss

        WHERE company_id=?

        ORDER BY year
        """,
        (company_id,),
    )

    return cursor.fetchall()


def extract_history(history_rows, column):

    values = []

    for row in history_rows:
        value = row[column]

        if value is not None:
            values.append(value)

    return values


def calculate_all_cagrs(history_rows):

    sales_history = extract_history(history_rows, "sales")
    pat_history = extract_history(history_rows, "net_profit")
    eps_history = extract_history(history_rows, "eps")

    revenue5, revenue_flag = calculate_metric_cagr(
        sales_history,
        5,
    )

    pat5, pat_flag = calculate_metric_cagr(
        pat_history,
        5,
    )

    eps5, eps_flag = calculate_metric_cagr(
        eps_history,
        5,
    )

    return {
        "revenue_cagr_5yr": revenue5,
        "revenue_cagr_flag": revenue_flag.value,
        "pat_cagr_5yr": pat5,
        "pat_cagr_flag": pat_flag.value,
        "eps_cagr_5yr": eps5,
        "eps_cagr_flag": eps_flag.value,
    }


# ==========================================================
# Process One Company-Year
# ==========================================================


def process_record(conn, row):
    """
    Compute all KPIs for a single company-year.
    """

    history_rows = load_company_history(
        conn,
        row["company_id"],
    )

    profitability = calculate_ratios(
        company=row["company_name"],
        year=row["year"],
        sales=row["sales"] or 0,
        net_profit=row["net_profit"] or 0,
        operating_profit=row["operating_profit"] or 0,
        other_income=row["other_income"] or 0,
        interest=row["interest"] or 0,
        opm_percentage=row["opm_percentage"],
        equity_capital=row["equity_capital"] or 0,
        reserves=row["reserves"] or 0,
        borrowings=row["borrowings"] or 0,
        investments=row["investments"] or 0,
        total_assets=row["total_assets"] or 0,
        broad_sector=row["broad_sector"] or "",
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

    cagrs = calculate_all_cagrs(history_rows)

    score = 0

    roe = profitability.get("return_on_equity_pct")
    de = profitability.get("debt_to_equity")
    cfo = cashflow.get("cfo_quality_score")
    rev = cagrs.get("revenue_cagr_5yr")

    if roe is not None:
        if roe >= 20:
            score += 3
        elif roe >= 15:
            score += 2
        elif roe >= 10:
            score += 1

    if de is not None:
        if de < 0.5:
            score += 2
        elif de < 1:
            score += 1

    if cfo is not None:
        if cfo > 1:
            score += 2
        elif cfo >= 0.5:
            score += 1

    if rev is not None:
        if rev > 15:
            score += 2
        elif rev > 8:
            score += 1

    result = {}

    result.update(profitability)
    result.update(cashflow)
    result.update(cagrs)

    result["composite_quality_score"] = score

    return result


# ==========================================================
# Insert into financial_ratios
# ==========================================================


def insert_financial_ratio(conn, row, ratios):

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO financial_ratios(

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

            revenue_cagr_5yr,
            pat_cagr_5yr,
            eps_cagr_5yr,

            revenue_cagr_flag,
            pat_cagr_flag,
            eps_cagr_flag,

            composite_quality_score

        )

        VALUES(

            ?,?,
            ?,?,?,?,?,
            ?,?,?,?,
            ?,?,?,
            ?,?,?,?,?,?,?,
            ?,?,?,?,
            ?,?,?,
            ?,?,?,
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
                if row["equity_capital"] not in (None, 0)
                else None
            ),
            row["dividend_payout"],
            row["borrowings"],
            ratios.get("revenue_cagr_5yr"),
            ratios.get("pat_cagr_5yr"),
            ratios.get("eps_cagr_5yr"),
            ratios.get("revenue_cagr_flag"),
            ratios.get("pat_cagr_flag"),
            ratios.get("eps_cagr_flag"),
            ratios.get("composite_quality_score"),
        ),
    )


# ==========================================================
# Capital Allocation CSV
# ==========================================================


def write_capital_allocation_csv(records):
    """
    Generate output/capital_allocation.csv
    """

    output_file = OUTPUT_DIR / "capital_allocation.csv"

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.writer(file)

        writer.writerow(
            [
                "company_id",
                "year",
                "cfo_sign",
                "cfi_sign",
                "cff_sign",
                "pattern_label",
            ]
        )

        writer.writerows(records)

    print(f"\nCapital allocation file created:")
    print(output_file)


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":
    conn = get_connection()

    rows = fetch_financial_data(conn)

    cursor = conn.cursor()

    cursor.execute("DELETE FROM financial_ratios")

    inserted = 0
    capital_records = []

    for row in rows:
        ratios = process_record(conn, row)
        capital_records.append(
            [
                row["company_id"],
                row["year"],
                "+" if (row["operating_activity"] or 0) >= 0 else "-",
                "+" if (row["investing_activity"] or 0) >= 0 else "-",
                "+" if (row["financing_activity"] or 0) >= 0 else "-",
                ratios.get("capital_allocation_pattern"),
            ]
        )

        insert_financial_ratio(
            conn,
            row,
            ratios,
        )

        inserted += 1

    conn.commit()
    write_capital_allocation_csv(capital_records)

    print("\n====================================")
    print("Financial Ratio Engine")
    print("====================================")
    print(f"Rows Processed : {len(rows)}")
    print(f"Rows Inserted  : {inserted}")
    print("====================================")

    conn.close()
