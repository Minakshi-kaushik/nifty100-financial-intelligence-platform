"""
Sprint 3

Stock Screener Engine

Loads:
    • SQLite financial ratios
    • Companies
    • Sectors
    • YAML configuration

Applies threshold filters
Returns filtered dataframe
"""

from pathlib import Path
import sqlite3
from src.screener.score import compute_composite_score

import pandas as pd
import yaml


BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "db" / "nifty100.db"

CONFIG_PATH = BASE_DIR / "config" / "screener_config.yaml"


def get_connection():

    conn = sqlite3.connect(DB_PATH)

    return conn


def load_financial_data():

    conn = get_connection()

    query = """
    SELECT

        fr.*,

        c.company_name,

        s.broad_sector

    FROM financial_ratios fr

    LEFT JOIN companies c
    ON fr.company_id = c.id

    LEFT JOIN sectors s
    ON fr.company_id = s.company_id
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


def load_config():

    with open(CONFIG_PATH, "r") as file:
        return yaml.safe_load(file)


def apply_min_filter(df, column, value):

    if value is None:
        return df

    return df[df[column] >= value]


def apply_max_filter(df, column, value):

    if value is None:
        return df

    return df[df[column] <= value]


def apply_de_filter(df, maximum):

    if maximum is None:
        return df

    financials = df["broad_sector"] == "Financials"

    passed = df["debt_to_equity"] <= maximum

    return df[financials | passed]


def apply_icr_filter(df, minimum):

    if minimum is None:
        return df

    debt_free = df["icr_label"] == "Debt Free"

    passed = df["interest_coverage"] >= minimum

    return df[debt_free | passed]


def apply_filters(df, filters):

    for key, value in filters.items():
        if key == "roe_min":
            df = apply_min_filter(
                df,
                "return_on_equity_pct",
                value,
            )

        elif key == "free_cash_flow_min":
            df = apply_min_filter(
                df,
                "free_cash_flow_cr",
                value,
            )

        elif key == "revenue_cagr_5yr_min":
            df = apply_min_filter(
                df,
                "revenue_cagr_5yr",
                value,
            )

        elif key == "pat_cagr_5yr_min":
            df = apply_min_filter(
                df,
                "pat_cagr_5yr",
                value,
            )

        elif key == "eps_cagr_5yr_min":
            df = apply_min_filter(
                df,
                "eps_cagr_5yr",
                value,
            )

        elif key == "opm_min":
            df = apply_min_filter(
                df,
                "operating_profit_margin_pct",
                value,
            )

        elif key == "sales_min":
            if "sales" in df.columns:
                df = apply_min_filter(
                    df,
                    "sales",
                    value,
                )

        elif key == "asset_turnover_min":
            df = apply_min_filter(
                df,
                "asset_turnover",
                value,
            )

        elif key == "debt_to_equity_max":
            df = apply_de_filter(
                df,
                value,
            )

        elif key == "interest_coverage_min":
            df = apply_icr_filter(
                df,
                value,
            )

        elif key == "dividend_payout_max":
            df = apply_max_filter(
                df,
                "dividend_payout_ratio_pct",
                value,
            )

    return df


def run_preset(name):

    config = load_config()

    df = load_financial_data()

    filters = config[name]

    print("\n===== DATA SUMMARY =====")
    print(
        df[
            [
                "return_on_equity_pct",
                "debt_to_equity",
                "free_cash_flow_cr",
                "revenue_cagr_5yr",
                "broad_sector",
            ]
        ].describe(include="all")
    )
    print("========================\n")

    print(f"\nInitial rows : {len(df)}")

    for key, value in filters.items():
        before = len(df)

        df = apply_filters(df, {key: value})

        after = len(df)

        print(f"{key} = {value} : {before} -> {after}")

    result = df

    # result = apply_filters(
    #     df,
    #     filters,
    # )
    result["composite_quality_score"] = compute_composite_score(result)

    result = result.sort_values(
        by="composite_quality_score",
        ascending=False,
    )
    result = result.reset_index(drop=True)

    print(f"\nCompanies Returned : {len(result)}")

    return result


if __name__ == "__main__":
    companies = run_preset("quality_compounder")

    print("=" * 70)
    print("QUALITY COMPOUNDER")
    print("=" * 70)

    cols = [
        "company_id",
        "company_name",
        "return_on_equity_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "free_cash_flow_cr",
        "composite_quality_score",
    ]

    print(companies[cols].head(20))
