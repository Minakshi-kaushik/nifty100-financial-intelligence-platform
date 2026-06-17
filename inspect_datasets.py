from pathlib import Path
import pandas as pd

DATA_DIR = Path("data/raw")

for file in DATA_DIR.glob("*.xlsx"):
    print("\n" + "=" * 80)
    print(f"FILE: {file.name}")

    try:
        xl = pd.ExcelFile(file)

        print("\nSheets:")
        print(xl.sheet_names)

        for sheet in xl.sheet_names:
            print("\n" + "-" * 50)
            print(f"SHEET: {sheet}")

            df = pd.read_excel(file, sheet_name=sheet)

            print(f"Rows: {df.shape[0]}")
            print(f"Columns: {df.shape[1]}")

            print("\nColumn Names:")
            print(df.columns.tolist())

            print("\nData Types:")
            print(df.dtypes)

            print("\nMissing Values:")
            print(df.isnull().sum())

            print("\nFirst 5 Rows:")
            print(df.head())

    except Exception as e:
        print(f"ERROR: {e}")
