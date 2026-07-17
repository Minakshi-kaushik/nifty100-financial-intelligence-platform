import streamlit as st
import plotly.graph_objects as go

from dashboard.utils.db import (
    get_peer_groups,
    get_ratios,
)

st.set_page_config(layout="wide")

st.title("👥 Peer Comparison")

peer_df = get_peer_groups()
ratios = get_ratios()

peer_names = sorted(peer_df["peer_group_name"].dropna().unique())

selected_peer = st.selectbox(
    "Select Peer Group",
    peer_names,
)

companies = peer_df[peer_df["peer_group_name"] == selected_peer]["company_id"]

peer_ratios = ratios[ratios["company_id"].isin(companies)]

company = st.selectbox("Select Company", sorted(peer_ratios["company_id"].unique()))

company_data = peer_ratios[peer_ratios["company_id"] == company].iloc[-1]

peer_avg = peer_ratios.groupby("company_id").last()

metrics = [
    "return_on_equity_pct",
    "return_on_capital_employed_pct",
    "net_profit_margin_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "pat_cagr_5yr",
    "revenue_cagr_5yr",
    "composite_quality_score",
]

peer_mean = peer_avg[metrics].mean()

fig = go.Figure()

fig.add_trace(
    go.Scatterpolar(
        r=company_data[metrics].values,
        theta=metrics,
        fill="toself",
        name=company,
    )
)

fig.add_trace(
    go.Scatterpolar(
        r=peer_mean.values,
        theta=metrics,
        fill="toself",
        name="Peer Average",
    )
)

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
        )
    ),
    showlegend=True,
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

st.divider()

st.subheader("Peer KPI Table")

columns = [
    c
    for c in [
        "company_id",
        "company_name",
        "return_on_equity_pct",
        "return_on_capital_employed_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "free_cash_flow_cr",
        "revenue_cagr_5yr",
        "composite_quality_score",
    ]
    if c in peer_ratios.columns
]

latest = peer_ratios.sort_values("year").groupby("company_id").last().reset_index()

st.dataframe(
    latest[columns],
    use_container_width=True,
    hide_index=True,
)
