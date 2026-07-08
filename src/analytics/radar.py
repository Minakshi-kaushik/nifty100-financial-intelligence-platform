"""
Sprint 3

Radar Chart Generator

Generates one radar chart for the latest available year
for every company using peer-group normalized metrics.
"""

from pathlib import Path
import sqlite3

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "db" / "nifty100.db"

OUTPUT = BASE_DIR / "reports" / "radar_charts"
OUTPUT.mkdir(parents=True, exist_ok=True)


YEAR_PRIORITY = {
    "Dec 2012": 2012,
    "Mar 2013": 2013,
    "Mar 2014": 2014,
    "Mar 2015": 2015,
    "Mar 2016": 2016,
    "Mar 2017": 2017,
    "Mar 2018": 2018,
    "Mar 2019": 2019,
    "Mar 2020": 2020,
    "Mar 2021": 2021,
    "Mar 2022": 2022,
    "Mar 2023": 2023,
    "Mar 2024": 2024,
    "Sep 2024": 2024.5,
    "TTM": 2025,
}


METRICS = [
    "return_on_equity_pct",
    "return_on_capital_employed_pct",
    "net_profit_margin_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "pat_cagr_5yr",
    "revenue_cagr_5yr",
    "composite_quality_score",
]


LABELS = [
    "ROE",
    "ROCE",
    "NPM",
    "D/E",
    "FCF",
    "PAT CAGR",
    "Revenue CAGR",
    "Score",
]


def load_data():

    conn = sqlite3.connect(DB_PATH)

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

    df = df.dropna(subset=["year"])

    df["year_order"] = df["year"].map(YEAR_PRIORITY)

    df = df.sort_values("year_order").groupby("company_id", as_index=False).last()

    df.drop(columns="year_order", inplace=True)

    return df


def normalize(group):

    data = group.copy()

    for col in METRICS:
        data[col] = data[col].fillna(0)

        mn = data[col].min()
        mx = data[col].max()

        if mx > mn:
            data[col] = (data[col] - mn) / (mx - mn)

        else:
            data[col] = 0.5

    return data


def create_chart(company_name, company_values, peer_average, filename):

    angles = np.linspace(
        0,
        2 * np.pi,
        len(LABELS),
        endpoint=False,
    )

    company_values = np.concatenate((company_values, [company_values[0]]))

    peer_average = np.concatenate((peer_average, [peer_average[0]]))

    angles = np.concatenate((angles, [angles[0]]))

    plt.figure(figsize=(7, 7))

    ax = plt.subplot(111, polar=True)

    ax.plot(
        angles,
        company_values,
        linewidth=2,
        label="Company",
    )

    ax.fill(
        angles,
        company_values,
        alpha=0.25,
    )

    ax.plot(
        angles,
        peer_average,
        linestyle="--",
        linewidth=2,
        label="Peer Average",
    )

    ax.set_xticks(angles[:-1])

    ax.set_xticklabels(
        LABELS,
        fontsize=9,
    )

    ax.set_title(
        company_name,
        fontsize=13,
        pad=20,
    )

    ax.legend(loc="upper right")

    plt.savefig(
        filename,
        dpi=150,
        bbox_inches="tight",
    )

    plt.close()


def generate():

    df = load_data()

    generated = 0

    for peer_name, group in df.groupby("peer_group_name"):
        if pd.isna(peer_name):
            continue

        if len(group) < 2:
            continue

        group = normalize(group)

        peer_average = group[METRICS].mean().values

        for _, row in group.iterrows():
            print(f"Generating {row['company_id']}...")

            create_chart(
                row["company_name"],
                row[METRICS].values,
                peer_average,
                OUTPUT / f"{row['company_id']}_radar.png",
            )

            generated += 1

    print("\n" + "=" * 60)
    print("Radar Charts Generated")
    print("=" * 60)
    print(f"Charts Generated : {generated}")
    print(f"Saved To         : {OUTPUT}")


if __name__ == "__main__":
    generate()
