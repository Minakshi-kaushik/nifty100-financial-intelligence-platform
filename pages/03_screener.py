import streamlit as st

from dashboard.utils.db import get_screener_data

st.title("📊 Stock Screener")

df = get_screener_data()

st.sidebar.header("Filters")

roe = st.sidebar.slider(
    "Minimum ROE",
    0.0,
    50.0,
    15.0,
)

de = st.sidebar.slider(
    "Maximum Debt/Equity",
    0.0,
    5.0,
    1.0,
)

rev = st.sidebar.slider(
    "Minimum Revenue CAGR",
    -20.0,
    50.0,
    5.0,
)

filtered = df[
    (df["return_on_equity_pct"] >= roe)
    & (df["debt_to_equity"] <= de)
    & (df["revenue_cagr_5yr"] >= rev)
]

st.subheader(f"Matching Companies : {len(filtered)}")

cols = [
    c
    for c in [
        "company_name",
        "broad_sector",
        "return_on_equity_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "composite_quality_score",
    ]
    if c in filtered.columns
]

st.dataframe(
    filtered[cols],
    use_container_width=True,
)

csv = filtered.to_csv(index=False)

st.download_button(
    "⬇ Download CSV",
    csv,
    file_name="screener_output.csv",
    mime="text/csv",
)
