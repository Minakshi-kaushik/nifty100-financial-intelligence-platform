import pandas as pd
from pathlib import Path

for file in [
    "analysis.xlsx",
    "financial_ratios.xlsx",
    "market_cap.xlsx",
    "peer_groups.xlsx",
    "prosandcons.xlsx",
    "sectors.xlsx",
    "stock_prices.xlsx",
]:
    print("\n" + "=" * 80)
    print(file)

    df = pd.read_excel(Path("data/raw") / file, header=1)

    for i, col in enumerate(df.columns, start=1):
        print(f"{i:02d}. {col}")

    print("Shape:", df.shape)
