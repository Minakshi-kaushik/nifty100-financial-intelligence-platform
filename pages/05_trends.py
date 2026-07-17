import streamlit as st
import plotly.express as px

from dashboard.utils.db import get_companies, get_ratios

st.set_page_config(layout="wide")

st.title("📈 Trend Analysis")

companies = get_companies()
ratios = get_ratios()

company = st.selectbox("Company", companies["company_name"])

metrics = st.multiselect(
    "Metrics",
    [
        "return_on_equity_pct",
        "return_on_capital_employed_pct",
        "net_profit_margin_pct",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
    ],
    default=["return_on_equity_pct"],
)

ticker = companies.loc[
    companies["company_name"] == company,
    "id",
].iloc[0]

df = ratios[ratios["company_id"] == ticker]

for metric in metrics:
    fig = px.line(
        df,
        x="year",
        y=metric,
        markers=True,
        title=metric,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )
