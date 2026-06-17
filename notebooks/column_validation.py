import pandas as pd

FILES = {
    "profitandloss.xlsx": 1,
    "balancesheet.xlsx": 1,
    "cashflow.xlsx": 1,
    "companies.xlsx": 1,
    "documents.xlsx": 1,
}

for file, header in FILES.items():
    print("\n" + "=" * 80)
    print(file)

    df = pd.read_excel(f"data/raw/{file}", header=header)

    print("\nColumns:")
    for idx, col in enumerate(df.columns, start=1):
        print(f"{idx:02d}. {col}")
