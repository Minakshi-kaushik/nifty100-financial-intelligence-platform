import streamlit as st
import plotly.express as px

from dashboard.utils.db import get_sector_analysis

st.title("🏭 Sector Analysis")

df = get_sector_analysis()

sector = st.selectbox("Sector", sorted(df["broad_sector"].dropna().unique()))

df = df[df["broad_sector"] == sector]

# Remove invalid market caps
df["market_cap_crore"] = df["market_cap_crore"].fillna(0).clip(lower=1)

fig = px.scatter(
    df,
    x="revenue_cagr_5yr",
    y="return_on_equity_pct",
    size="market_cap_crore",
    color="sub_sector",
    hover_name="company_id",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

st.subheader("Sector Median")

median = (
    df[
        [
            "return_on_equity_pct",
            "revenue_cagr_5yr",
        ]
    ]
    .median()
    .reset_index()
)

median.columns = ["Metric", "Median"]

fig2 = px.bar(
    median,
    x="Metric",
    y="Median",
)

st.plotly_chart(
    fig2,
    use_container_width=True,
)
