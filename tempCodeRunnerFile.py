import sqlite3

conn = sqlite3.connect("db/nifty100.db")

tables = [
    "companies",
    "profitandloss",
    "balancesheet",
    "cashflow",
    "analysis",
    "documents",
    "financial_ratios",
    "market_cap",
    "peer_groups",
    "sectors",
    "prosandcons",
    "stock_prices"
]

for t in tables:
    count = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    print(f"{t}: {count}")

conn.close()