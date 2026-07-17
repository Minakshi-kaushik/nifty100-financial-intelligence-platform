import streamlit as st
import plotly.express as px

from dashboard.utils.db import get_ratios

st.set_page_config(layout="wide")

st.title("🌳 Capital Allocation")

df = get_ratios()

if "capital_allocation_pattern" in df.columns:
    fig = px.treemap(
        df,
        path=["capital_allocation_pattern", "company_id"],
        values="free_cash_flow_cr",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

else:
    st.info("Capital allocation labels unavailable.")
