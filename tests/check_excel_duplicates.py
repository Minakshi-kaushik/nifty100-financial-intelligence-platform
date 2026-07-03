from pathlib import Path
import pandas as pd

DATA_DIR = Path("data/raw")

files = [
    "profitandloss.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
]

headers = {
    "profitandloss.xlsx": 1,
    "balancesheet.xlsx": 1,
    "cashflow.xlsx": 1,
}

for file in files:
    print("\n" + "=" * 60)
    print(file)

    df = pd.read_excel(DATA_DIR / file, header=headers[file])

    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    dup = df[df.duplicated(subset=["company_id", "year"], keep=False)]

    print("Duplicate rows:", len(dup))

    if len(dup):
        print(dup[["company_id", "year"]].sort_values(["company_id", "year"]))
