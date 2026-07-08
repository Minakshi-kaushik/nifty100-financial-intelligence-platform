from pathlib import Path
import sqlite3

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "db" / "nifty100.db"


def get_connection():

    conn = sqlite3.connect(DB_PATH)

    return conn


def load_data():

    conn = get_connection()

    query = """
    SELECT

        fr.*,

        pg.peer_group_name,

        c.company_name

    FROM financial_ratios fr

    LEFT JOIN peer_groups pg
    ON fr.company_id = pg.company_id

    LEFT JOIN companies c
    ON fr.company_id = c.id
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


def compute_percentile(series, ascending=True):

    return (
        series.rank(
            pct=True,
            ascending=ascending,
            na_option="bottom",
        )
        * 100
    )


METRICS = {
    "return_on_equity_pct": False,
    "return_on_capital_employed_pct": False,
    "net_profit_margin_pct": False,
    "debt_to_equity": True,
    "free_cash_flow_cr": False,
    "pat_cagr_5yr": False,
    "revenue_cagr_5yr": False,
    "eps_cagr_5yr": False,
    "interest_coverage": False,
    "asset_turnover": False,
}


def build_peer_percentiles(df):

    records = []

    groups = df.groupby("peer_group_name")

    for group_name, group in groups:
        for metric, inverse in METRICS.items():
            temp = group.copy()

            if inverse:
                temp["percentile"] = 100 - compute_percentile(temp[metric])

            else:
                temp["percentile"] = compute_percentile(temp[metric])

            for _, row in temp.iterrows():
                records.append(
                    {
                        "company_id": row["company_id"],
                        "peer_group_name": group_name,
                        "metric": metric,
                        "value": row[metric],
                        "percentile_rank": round(
                            row["percentile"],
                            2,
                        ),
                        "year": row["year"],
                    }
                )

    return pd.DataFrame(records)


def compute_peer_percentiles():
    """
    Loads financial data, computes peer percentile rankings,
    saves them to SQLite, and returns the DataFrame.
    """

    df = load_data()

    result = build_peer_percentiles(df)

    save(result)

    return result


def save(df):

    conn = get_connection()

    df.to_sql(
        "peer_percentiles",
        conn,
        if_exists="replace",
        index=False,
    )

    conn.close()


if __name__ == "__main__":
    result = compute_peer_percentiles()

    print(result.head())

    print()

    print("Rows :", len(result))
