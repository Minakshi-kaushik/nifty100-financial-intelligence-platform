import streamlit as st

from dashboard.utils.db import (
    get_companies,
    run_query,
)

st.set_page_config(layout="wide")

st.title("📄 Annual Reports")

companies = get_companies()

company = st.selectbox(
    "Company",
    companies["company_name"],
)

ticker = companies.loc[
    companies["company_name"] == company,
    "id",
].iloc[0]

query = """
SELECT *
FROM documents
WHERE company_id=?
ORDER BY year DESC
"""

docs = run_query(
    query,
    [ticker],
)

if len(docs) == 0:
    st.warning("No reports available.")

else:
    if "annual_report_link" in docs.columns:
        docs["annual_report_link"] = docs["annual_report_link"].apply(
            lambda x: f"[Open Report]({x})"
        )

    st.dataframe(
        docs,
        use_container_width=True,
    )
