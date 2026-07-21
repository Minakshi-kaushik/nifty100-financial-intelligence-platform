"""
parser.py

Parses CAGR text from analysis table into structured format.

Outputs:
---------
output/analysis_parsed.csv
output/parse_failures.csv
"""

import re
import sqlite3
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "db" / "nifty100.db"

OUTPUT = BASE_DIR / "output"
OUTPUT.mkdir(exist_ok=True)


PATTERN = re.compile(
    r"(\d+)\s*Years?\s*:?\s*([\d\.]+)\s*%",
    re.IGNORECASE,
)


def parse_text(text):
    """
    Returns:
        [(period,value),...]
    """

    if text is None:
        return []

    matches = PATTERN.findall(str(text))

    return [
        (
            int(period),
            float(value),
        )
        for period, value in matches
    ]


def load_analysis():

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        """
        SELECT *
        FROM analysis
        """,
        conn,
    )

    conn.close()

    return df


def build():

    analysis = load_analysis()

    parsed_rows = []

    failures = []

    metric_columns = [
        "compounded_sales_growth",
        "compounded_profit_growth",
        "stock_price_cagr",
        "roe",
    ]

    for _, row in analysis.iterrows():
        company = row["company_id"]

        for metric in metric_columns:
            value = row[metric]

            parsed = parse_text(value)

            if len(parsed) == 0:
                failures.append(
                    {
                        "company_id": company,
                        "metric": metric,
                        "raw_text": value,
                    }
                )

            else:
                for years, pct in parsed:
                    parsed_rows.append(
                        {
                            "company_id": company,
                            "metric_type": metric,
                            "period_years": years,
                            "value_pct": pct,
                        }
                    )

    parsed_df = pd.DataFrame(parsed_rows)

    fail_df = pd.DataFrame(failures)

    return parsed_df, fail_df


def cross_validate(parsed):
    """
    Optional validation against Ratio Engine.

    Flags >5% differences if matching CAGR exists.
    """

    conn = sqlite3.connect(DB_PATH)

    ratios = pd.read_sql(
        """
        SELECT
            company_id,
            revenue_cagr_3yr,
            revenue_cagr_5yr,
            revenue_cagr_10yr,
            pat_cagr_3yr,
            pat_cagr_5yr,
            pat_cagr_10yr,
            eps_cagr_3yr,
            eps_cagr_5yr,
            eps_cagr_10yr
        FROM financial_ratios
        """,
        conn,
    )

    conn.close()

    validation = []

    for _, row in parsed.iterrows():
        cid = row["company_id"]

        yrs = row["period_years"]

        metric = row["metric_type"]

        actual = row["value_pct"]

        company = ratios[ratios.company_id == cid]

        if company.empty:
            continue

        company = company.iloc[0]

        expected = None

        if metric == "compounded_sales_growth":
            expected = company.get(f"revenue_cagr_{yrs}yr")

        elif metric == "compounded_profit_growth":
            expected = company.get(f"pat_cagr_{yrs}yr")

        elif metric == "stock_price_cagr":
            expected = company.get(f"eps_cagr_{yrs}yr")

        if expected is None or pd.isna(expected):
            continue

        diff = abs(actual - expected)

        if diff > 5:
            validation.append(
                {
                    "company_id": cid,
                    "metric": metric,
                    "years": yrs,
                    "parsed": actual,
                    "computed": expected,
                    "difference": diff,
                }
            )

    return pd.DataFrame(validation)


def main():

    parsed, failures = build()

    parsed.to_csv(
        OUTPUT / "analysis_parsed.csv",
        index=False,
    )

    failures.to_csv(
        OUTPUT / "parse_failures.csv",
        index=False,
    )

    validation = cross_validate(parsed)

    validation.to_csv(
        OUTPUT / "parse_validation.csv",
        index=False,
    )

    print("=" * 60)
    print("Analysis Parser Complete")
    print("=" * 60)
    print("Parsed :", len(parsed))
    print("Failures :", len(failures))
    print("Validation Flags :", len(validation))


if __name__ == "__main__":
    main()
