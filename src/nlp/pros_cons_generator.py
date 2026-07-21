from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "db" / "nifty100.db"

OUTPUT = BASE_DIR / "output"
OUTPUT.mkdir(exist_ok=True)


def load_data():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        fr.*,
        mc.dividend_yield_pct,
        c.company_name
    FROM financial_ratios fr

    LEFT JOIN market_cap mc
        ON fr.company_id = mc.company_id
        AND CAST(mc.year AS INTEGER)=2024

    LEFT JOIN companies c
        ON fr.company_id=c.id
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


def confidence(score):

    return max(
        60,
        min(
            100,
            int(score),
        ),
    )


def generate(df):

    rows = []

    latest = df.sort_values("year").groupby("company_id").tail(1)

    for _, r in latest.iterrows():
        cid = r.company_id

        ####################################################
        # PROS
        ####################################################

        if pd.notna(r.return_on_equity_pct):
            if r.return_on_equity_pct > 20:
                rows.append(
                    {
                        "company_id": cid,
                        "type": "Pro",
                        "rule_id": "P1",
                        "text": "Consistently high return on equity above 20% demonstrates exceptional capital efficiency.",
                        "confidence_pct": confidence(r.return_on_equity_pct * 3),
                    }
                )

        if pd.notna(r.free_cash_flow_cr):
            if r.free_cash_flow_cr > 0:
                rows.append(
                    {
                        "company_id": cid,
                        "type": "Pro",
                        "rule_id": "P2",
                        "text": "Positive free cash flow indicates healthy cash generation.",
                        "confidence_pct": 85,
                    }
                )

        if r.debt_to_equity == 0:
            rows.append(
                {
                    "company_id": cid,
                    "type": "Pro",
                    "rule_id": "P3",
                    "text": "Debt-free balance sheet provides financial flexibility and eliminates interest burden.",
                    "confidence_pct": 95,
                }
            )

        if pd.notna(r.operating_profit_margin_pct):
            if r.operating_profit_margin_pct > 25:
                rows.append(
                    {
                        "company_id": cid,
                        "type": "Pro",
                        "rule_id": "P5",
                        "text": "Operating margin above 25% indicates strong pricing power.",
                        "confidence_pct": 90,
                    }
                )

        if pd.notna(r.interest_coverage):
            if r.interest_coverage > 10:
                rows.append(
                    {
                        "company_id": cid,
                        "type": "Pro",
                        "rule_id": "P7",
                        "text": "Very high interest coverage reflects negligible debt servicing risk.",
                        "confidence_pct": 90,
                    }
                )

        if pd.notna(r.dividend_yield_pct):
            if r.dividend_yield_pct > 2:
                rows.append(
                    {
                        "company_id": cid,
                        "type": "Pro",
                        "rule_id": "P8",
                        "text": "Healthy dividend yield backed by business performance.",
                        "confidence_pct": 80,
                    }
                )

        ####################################################
        # CONS
        ####################################################

        if pd.notna(r.debt_to_equity):
            if r.debt_to_equity > 2:
                rows.append(
                    {
                        "company_id": cid,
                        "type": "Con",
                        "rule_id": "C1",
                        "text": "Debt-to-equity ratio is elevated and warrants monitoring.",
                        "confidence_pct": 90,
                    }
                )

        if pd.notna(r.free_cash_flow_cr):
            if r.free_cash_flow_cr < 0:
                rows.append(
                    {
                        "company_id": cid,
                        "type": "Con",
                        "rule_id": "C2",
                        "text": "Negative free cash flow raises concern about cash generation quality.",
                        "confidence_pct": 85,
                    }
                )

        if pd.notna(r.interest_coverage):
            if r.interest_coverage < 1.5:
                rows.append(
                    {
                        "company_id": cid,
                        "type": "Con",
                        "rule_id": "C6",
                        "text": "Interest coverage below 1.5x indicates elevated financial risk.",
                        "confidence_pct": 95,
                    }
                )

        if pd.notna(r.return_on_capital_employed_pct):
            if r.return_on_capital_employed_pct < 10:
                rows.append(
                    {
                        "company_id": cid,
                        "type": "Con",
                        "rule_id": "C10",
                        "text": "Low ROCE suggests weak capital efficiency.",
                        "confidence_pct": 75,
                    }
                )

    return pd.DataFrame(rows)


def ensure_every_company(df, companies):

    result = df.copy()

    for cid in companies:
        temp = result[result.company_id == cid]

        if not (temp.type == "Pro").any():
            result.loc[len(result)] = [
                cid,
                "Pro",
                "PX",
                "Stable business fundamentals.",
                60,
            ]

        if not (temp.type == "Con").any():
            result.loc[len(result)] = [
                cid,
                "Con",
                "CX",
                "No major risk detected from available metrics.",
                60,
            ]

    return result


def main():

    df = load_data()

    pros_cons = generate(df)

    companies = df.company_id.unique()

    pros_cons = ensure_every_company(
        pros_cons,
        companies,
    )

    pros_cons.to_csv(
        OUTPUT / "pros_cons_generated.csv",
        index=False,
    )

    print("=" * 60)

    print("Pros & Cons Generated")

    print("=" * 60)

    print(pros_cons.head())

    print()

    print("Total Rows :", len(pros_cons))


if __name__ == "__main__":
    main()
