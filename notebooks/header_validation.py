from pathlib import Path
import pandas as pd

DATA_DIR = Path("data/raw")

for file in DATA_DIR.glob("*.xlsx"):
    print("\n" + "=" * 80)
    print(f"FILE: {file.name}")

    for header in [0, 1, 2]:
        try:
            df = pd.read_excel(file, header=header)

            print(f"\nHEADER = {header}")
            print("Columns:")

            for col in df.columns:
                print(col)

            print("\nFirst 2 rows:")
            print(df.head(2))

        except Exception as e:
            print(f"Error with header={header}: {e}")
