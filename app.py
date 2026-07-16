import streamlit as st

st.set_page_config(
    page_title="Nifty 100 Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📈 Nifty 100 Analytics Dashboard")

st.markdown(
    """
Welcome to the **Nifty 100 Financial Analytics Dashboard**.

Use the **sidebar** to navigate between the dashboard pages.

### Available Screens

- 🏠 Home
- 🏢 Company Profile
- 🔍 Stock Screener
- 👥 Peer Comparison
- 📊 Trend Analysis
- 🏭 Sector Analysis
- 💰 Capital Allocation
- 📄 Annual Reports
"""
)

st.info("Select a page from the left sidebar to begin.")
