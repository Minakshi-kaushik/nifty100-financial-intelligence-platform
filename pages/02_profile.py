import streamlit as st

from dashboard.utils.db import (
    get_company_list,
    get_company_ratios,
    get_company_sector,
)

st.set_page_config(layout="wide")

st.title("🏢 Company Profile")

companies = get_company_list()

selected = st.selectbox("Select Company", companies["company_name"])

company_id = companies.loc[companies["company_name"] == selected, "id"].iloc[0]

sector = get_company_sector(company_id)
ratios = get_company_ratios(company_id)

st.divider()

left, right = st.columns([2, 1])

with left:
    st.subheader(selected)

    if not sector.empty:
        st.write(f"Sector : {sector.iloc[0]['broad_sector']}")

with right:
    if not ratios.empty:
        latest = ratios.iloc[-1]

        c1, c2, c3 = st.columns(3)

        c1.metric("ROE", f"{latest['return_on_equity_pct']:.2f}%")

        c2.metric("ROCE", f"{latest['return_on_capital_employed_pct']:.2f}%")

        c3.metric("D/E", f"{latest['debt_to_equity']:.2f}")

# st.dataframe(
#     ratios,
#     use_container_width=True,
#     hide_index=True,
# )
