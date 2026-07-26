"""
clustering.py

Sprint 6
Day 36 & Day 37

KMeans clustering
Cluster profiling
Correlation heatmap
Outlier detection
Portfolio statistics
"""

from pathlib import Path
import sqlite3

import numpy as np
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

import matplotlib.pyplot as plt
import seaborn as sns


# =====================================================
# PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "db" / "nifty100.db"

OUTPUT_DIR = BASE_DIR / "output"

REPORT_DIR = BASE_DIR / "reports"

OUTPUT_DIR.mkdir(exist_ok=True)

REPORT_DIR.mkdir(exist_ok=True)


# =====================================================
# DATABASE
# =====================================================


def query(sql):

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(sql, conn)

    conn.close()

    return df


# =====================================================
# LOAD DATA
# =====================================================


def load_data():

    sql = """
    SELECT

        fr.company_id,

        s.broad_sector,

        fr.return_on_equity_pct,

        fr.debt_to_equity,

        fr.revenue_cagr_5yr,

        fr.operating_profit_margin_pct,

        fr.free_cash_flow_cr,

        fr.composite_quality_score

    FROM financial_ratios fr

    JOIN sectors s

        ON fr.company_id=s.company_id

    WHERE fr.year='Mar 2024'
    """

    return query(sql)


FEATURES = [
    "return_on_equity_pct",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "operating_profit_margin_pct",
    "free_cash_flow_cr",
]


# =====================================================
# SECTOR MEDIAN IMPUTATION
# =====================================================


def impute_missing(df):

    df = df.copy()

    for col in FEATURES:
        df[col] = df.groupby("broad_sector")[col].transform(
            lambda x: x.fillna(x.median())
        )

    imputer = SimpleImputer(strategy="median")

    df[FEATURES] = imputer.fit_transform(df[FEATURES])

    return df


# =====================================================
# SCALING
# =====================================================


def scale_features(df):

    scaler = StandardScaler()

    scaled = scaler.fit_transform(df[FEATURES])

    return scaled


# =====================================================
# ELBOW PLOT
# =====================================================


def elbow_plot(data):

    inertia = []

    ks = range(2, 11)

    for k in ks:
        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10,
        )

        model.fit(data)

        inertia.append(model.inertia_)

    plt.figure(figsize=(7, 5))

    plt.plot(
        ks,
        inertia,
        marker="o",
    )

    plt.title("KMeans Elbow Curve")

    plt.xlabel("Number of Clusters")

    plt.ylabel("Inertia")

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        REPORT_DIR / "elbow_plot.png",
        dpi=300,
    )

    plt.close()


# =====================================================
# RUN KMEANS
# =====================================================


def run_kmeans(df):

    scaled = scale_features(df)

    model = KMeans(
        n_clusters=5,
        random_state=42,
        n_init=10,
    )

    clusters = model.fit_predict(scaled)

    distances = np.linalg.norm(
        scaled - model.cluster_centers_[clusters],
        axis=1,
    )

    df["cluster_id"] = clusters

    df["distance_from_centroid"] = distances

    return df, model


# =====================================================
# CLUSTER NAMES
# =====================================================

CLUSTER_NAMES = {
    0: "High-Quality Compounders",
    1: "Defensive Dividend Payers",
    2: "Emerging Growth",
    3: "Value Cyclicals",
    4: "Distressed / Turnaround",
}


def assign_cluster_names(df):

    df["cluster_name"] = df["cluster_id"].map(CLUSTER_NAMES)

    return df


# =====================================================
# SAVE CLUSTER LABELS
# =====================================================


def save_cluster_labels(df):

    cols = [
        "company_id",
        "cluster_id",
        "cluster_name",
        "distance_from_centroid",
    ]

    df[cols].to_csv(
        OUTPUT_DIR / "cluster_labels.csv",
        index=False,
    )


# =====================================================
# CORRELATION HEATMAP
# =====================================================


def correlation_heatmap(df):

    corr_cols = FEATURES + [
        "composite_quality_score",
    ]

    corr = df[corr_cols].corr(method="pearson")

    plt.figure(figsize=(10, 8))

    sns.heatmap(
        corr,
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
    )

    plt.title("Correlation Matrix")

    plt.tight_layout()

    plt.savefig(
        REPORT_DIR / "correlation_heatmap.png",
        dpi=300,
    )

    plt.close()


# =====================================================
# OUTLIER REPORT
# =====================================================


def outlier_report(df):

    rows = []

    for sector in df["broad_sector"].unique():
        temp = df[df["broad_sector"] == sector].copy()

        for metric in FEATURES:
            std = temp[metric].std()

            if std == 0 or pd.isna(std):
                continue

            mean = temp[metric].mean()

            z = (temp[metric] - mean) / std

            temp[f"{metric}_z"] = z

            outliers = temp[abs(z) > 3]

            for _, r in outliers.iterrows():
                rows.append(
                    {
                        "company_id": r["company_id"],
                        "sector": sector,
                        "metric": metric,
                        "value": r[metric],
                        "z_score": r[f"{metric}_z"],
                    }
                )

    pd.DataFrame(rows).to_csv(
        OUTPUT_DIR / "outlier_report.csv",
        index=False,
    )


# =====================================================
# PORTFOLIO STATISTICS
# =====================================================


def portfolio_statistics(df):

    stats = []

    metrics = FEATURES + [
        "composite_quality_score",
    ]

    for metric in metrics:
        series = df[metric].dropna()

        stats.append(
            {
                "metric": metric,
                "P10": series.quantile(0.10),
                "P25": series.quantile(0.25),
                "P50": series.quantile(0.50),
                "P75": series.quantile(0.75),
                "P90": series.quantile(0.90),
                "Mean": series.mean(),
                "Std": series.std(),
            }
        )

    pd.DataFrame(stats).to_csv(
        OUTPUT_DIR / "portfolio_stats.csv",
        index=False,
    )


# =====================================================
# CLUSTER PROFILE
# =====================================================


def cluster_profile(df):

    profile = df.groupby("cluster_name")[FEATURES].agg(["mean", "median"]).round(2)

    profile.to_csv(OUTPUT_DIR / "cluster_profile.csv")


# =====================================================
# MAIN
# =====================================================


def main():

    print("=" * 60)

    print("Running KMeans Clustering")

    print("=" * 60)

    df = load_data()

    print(f"Loaded {len(df)} companies")

    df = impute_missing(df)

    elbow_plot(scale_features(df))

    df, model = run_kmeans(df)

    df = assign_cluster_names(df)

    save_cluster_labels(df)

    correlation_heatmap(df)

    outlier_report(df)

    portfolio_statistics(df)

    cluster_profile(df)

    print()

    print("=" * 60)

    print("SPRINT 6 DAY 36-37 COMPLETE")

    print("=" * 60)

    print("Generated Files")

    print()

    print("output/cluster_labels.csv")

    print("output/cluster_profile.csv")

    print("output/outlier_report.csv")

    print("output/portfolio_stats.csv")

    print("reports/elbow_plot.png")

    print("reports/correlation_heatmap.png")

    print("=" * 60)


# =====================================================
# ENTRY POINT
# =====================================================

if __name__ == "__main__":
    main()
