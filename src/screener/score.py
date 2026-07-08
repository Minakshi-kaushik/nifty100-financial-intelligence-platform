"""
Sprint 3
Composite Quality Score
"""

import pandas as pd


def normalize(series):

    minimum = series.min()
    maximum = series.max()

    if pd.isna(minimum) or pd.isna(maximum):
        return pd.Series([0] * len(series), index=series.index)

    if maximum == minimum:
        return pd.Series([100] * len(series), index=series.index)

    return ((series - minimum) / (maximum - minimum)) * 100


def compute_composite_score(df):

    roe = normalize(df["return_on_equity_pct"])
    roce = normalize(df["return_on_capital_employed_pct"])
    npm = normalize(df["net_profit_margin_pct"])

    fcf = normalize(df["free_cash_flow_cr"])
    revenue = normalize(df["revenue_cagr_5yr"])
    pat = normalize(df["pat_cagr_5yr"])

    debt = 100 - normalize(df["debt_to_equity"])

    score = (
        roe * 0.20
        + roce * 0.15
        + npm * 0.15
        + fcf * 0.20
        + revenue * 0.15
        + pat * 0.10
        + debt * 0.05
    )

    return score.round(2)
