import streamlit as st
import plotly.express as px

from dashboard.utils.db import (
    get_companies,
    get_ratios,
    get_sectors,
)

st.set_page_config(layout="wide")

st.title("🏠 Home Dashboard")

companies = get_companies()
ratios = get_ratios()
sectors = get_sectors()

# -------------------------------
# Sidebar Filters
# -------------------------------

st.sidebar.header("Dashboard Filters")

years = sorted(
    ratios["year"].dropna().unique(),
    reverse=True,
)

selected_year = st.sidebar.selectbox(
    "Financial Year",
    years,
)

ratios = ratios[ratios["year"] == selected_year]

st.header("Market Overview")

st.caption(f"Financial Year : {selected_year}")

c1, c2, c3, c4, c5, c6 = st.columns(6)

c1.metric(
    "Companies",
    len(companies),
)

c2.metric("Average ROE", f"{ratios['return_on_equity_pct'].mean():.2f}%")

c3.metric("Median D/E", f"{ratios['debt_to_equity'].median():.2f}")

c4.metric("Median Revenue CAGR", f"{ratios['revenue_cagr_5yr'].median():.2f}%")

c5.metric(
    "Median P/E",
    f"{ratios['price_to_earnings'].median():.2f}"
    if "price_to_earnings" in ratios.columns
    else "N/A",
)

debt_free = (
    (ratios["debt_to_equity"] == 0).sum() if "debt_to_equity" in ratios.columns else 0
)

c6.metric(
    "Debt Free",
    debt_free,
)

st.divider()

left, right = st.columns([2, 1])

with left:
    st.subheader("Sector Distribution")

    sector_counts = sectors.groupby("broad_sector").size().reset_index(name="Companies")

    fig = px.pie(
        sector_counts,
        names="broad_sector",
        values="Companies",
        hole=0.45,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

with right:
    st.subheader("Top Quality Companies")

    if "composite_quality_score" in ratios.columns:
        top = ratios.sort_values(
            "composite_quality_score",
            ascending=False,
        ).head(5)

        cols = [
            c
            for c in [
                "company_id",
                "company_name",
                "composite_quality_score",
                "return_on_equity_pct",
                "revenue_cagr_5yr",
                "debt_to_equity",
            ]
            if c in top.columns
        ]

        st.dataframe(
            top[cols],
            hide_index=True,
            use_container_width=True,
        )

    else:
        st.info("Composite Quality Score not available.")
