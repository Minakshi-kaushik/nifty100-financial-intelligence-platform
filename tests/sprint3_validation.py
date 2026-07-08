from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent

DB = BASE_DIR / "db" / "nifty100.db"

conn = sqlite3.connect(DB)

cur = conn.cursor()

print("=" * 60)
print("SPRINT 3 VALIDATION")
print("=" * 60)

tables = [
    "financial_ratios",
    "peer_percentiles",
]

for table in tables:
    cur.execute(f"SELECT COUNT(*) FROM {table}")

    print(table, cur.fetchone()[0])

conn.close()

print()

outputs = [
    BASE_DIR / "output" / "screener_output.xlsx",
    BASE_DIR / "output" / "peer_comparison.xlsx",
]

for file in outputs:
    print(file.name, file.exists())

print()

charts = BASE_DIR / "reports" / "radar_charts"

print("Radar Charts :", len(list(charts.glob("*.png"))))
