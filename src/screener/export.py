"""
Export Screener Results
"""

from pathlib import Path

import pandas as pd

from src.screener.presets import (
    quality_compounder,
    value_pick,
    growth_accelerator,
    dividend_champion,
    debt_free_bluechip,
    turnaround_watch,
)

OUTPUT = Path("output")
OUTPUT.mkdir(exist_ok=True)

writer = OUTPUT / "screener_output.xlsx"

with pd.ExcelWriter(writer) as excel:
    quality_compounder().to_excel(
        excel,
        sheet_name="Quality",
        index=False,
    )

    value_pick().to_excel(
        excel,
        sheet_name="Value",
        index=False,
    )

    growth_accelerator().to_excel(
        excel,
        sheet_name="Growth",
        index=False,
    )

    dividend_champion().to_excel(
        excel,
        sheet_name="Dividend",
        index=False,
    )

    debt_free_bluechip().to_excel(
        excel,
        sheet_name="DebtFree",
        index=False,
    )

    turnaround_watch().to_excel(
        excel,
        sheet_name="Turnaround",
        index=False,
    )

print("Export Complete")
print(writer)
