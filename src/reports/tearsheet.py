"""
tearsheet.py

Generate 2-page PDF tearsheets for all companies.
"""

from pathlib import Path
import sqlite3

import matplotlib.pyplot as plt
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# =====================================================
# PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "db" / "nifty100.db"

REPORT_DIR = BASE_DIR / "reports" / "tearsheets"

CHART_DIR = BASE_DIR / "reports" / "charts"

OUTPUT_DIR = BASE_DIR / "output"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

styles = getSampleStyleSheet()

# =====================================================
# DATABASE
# =====================================================


def query(sql, params=None):

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(
        sql,
        conn,
        params=params,
    )

    conn.close()

    return df


# =====================================================
# COMPANY
# =====================================================


def get_company(company):

    df = query(
        """
        SELECT *
        FROM companies
        WHERE id=?
        """,
        [company],
    )

    if df.empty:
        return None

    return df.iloc[0]


# =====================================================
# PROFIT & LOSS
# =====================================================


def get_profit(company):

    return query(
        """
        SELECT *
        FROM profitandloss
        WHERE company_id=?
        ORDER BY year
        """,
        [company],
    )


# =====================================================
# BALANCE SHEET
# =====================================================


def get_balance(company):

    return query(
        """
        SELECT *
        FROM balancesheet
        WHERE company_id=?
        ORDER BY year
        """,
        [company],
    )


# =====================================================
# CASHFLOW
# =====================================================


def get_cashflow(company):

    return query(
        """
        SELECT *
        FROM cashflow
        WHERE company_id=?
        ORDER BY year
        """,
        [company],
    )


# =====================================================
# RATIOS
# =====================================================


def get_ratios(company):

    return query(
        """
        SELECT *
        FROM financial_ratios
        WHERE company_id=?
        ORDER BY year
        """,
        [company],
    )


# =====================================================
# PROS & CONS
# =====================================================


def get_pros_cons(company):

    sql = """
    SELECT
        company_id,
        'pro' AS type,
        pros AS text
    FROM prosandcons
    WHERE company_id=?

    UNION ALL

    SELECT
        company_id,
        'con' AS type,
        cons AS text
    FROM prosandcons
    WHERE company_id=?
    """

    return query(
        sql,
        [company, company],
    )


# =====================================================
# VALIDATION
# =====================================================


def validate(company):

    company_info = get_company(company)

    profit = get_profit(company)

    balance = get_balance(company)

    cash = get_cashflow(company)

    ratios = get_ratios(company)

    if company_info is None:
        raise ValueError("Company not found")

    if profit.empty:
        raise ValueError("Profit data missing")

    if balance.empty:
        raise ValueError("Balance sheet missing")

    if cash.empty:
        raise ValueError("Cashflow missing")

    if ratios.empty:
        raise ValueError("Ratio data missing")

    return (
        company_info,
        profit,
        balance,
        cash,
        ratios,
    )


# =====================================================
# CHARTS
# =====================================================


def revenue_profit_chart(df, company):

    plt.figure(figsize=(7, 3))

    plt.bar(
        df["year"],
        df["sales"],
        label="Revenue",
    )

    plt.plot(
        df["year"],
        df["net_profit"],
        marker="o",
        linewidth=2,
        label="Net Profit",
    )

    plt.xticks(rotation=90)

    plt.legend()

    plt.tight_layout()

    path = CHART_DIR / f"{company}_revenue_profit.png"

    plt.savefig(path)

    plt.close()

    return path


def roe_roce_chart(ratio, company):

    plt.figure(figsize=(7, 3))

    if "return_on_equity_pct" in ratio.columns:
        plt.plot(
            ratio["year"],
            ratio["return_on_equity_pct"],
            marker="o",
            linewidth=2,
            label="ROE",
        )

    if "return_on_capital_employed_pct" in ratio.columns:
        plt.plot(
            ratio["year"],
            ratio["return_on_capital_employed_pct"],
            marker="o",
            linewidth=2,
            label="ROCE",
        )

    plt.xticks(rotation=90)

    plt.legend()

    plt.tight_layout()

    path = CHART_DIR / f"{company}_roe_roce.png"

    plt.savefig(path)

    plt.close()

    return path


def balance_chart(df, company):

    plt.figure(figsize=(7, 3))

    plt.bar(
        df["year"],
        df["equity_capital"],
        label="Equity",
    )

    plt.bar(
        df["year"],
        df["borrowings"],
        bottom=df["equity_capital"],
        label="Borrowings",
    )

    plt.bar(
        df["year"],
        df["other_liabilities"],
        bottom=df["equity_capital"] + df["borrowings"],
        label="Other Liabilities",
    )

    plt.legend()

    plt.xticks(rotation=90)

    plt.tight_layout()

    path = CHART_DIR / f"{company}_balance.png"

    plt.savefig(path)

    plt.close()

    return path


def cashflow_chart(df, company):

    latest = df.iloc[-1]

    labels = [
        "Operating",
        "Investing",
        "Financing",
        "Net",
    ]

    values = [
        latest["operating_activity"],
        latest["investing_activity"],
        latest["financing_activity"],
        latest["net_cash_flow"],
    ]

    plt.figure(figsize=(6, 3))

    plt.bar(
        labels,
        values,
    )

    plt.tight_layout()

    path = CHART_DIR / f"{company}_cashflow.png"

    plt.savefig(path)

    plt.close()

    return path


# =====================================================
# KPI TABLE
# =====================================================


def kpi_table(company, ratio):

    latest = ratio.iloc[-1]

    data = [
        [
            "ROE",
            f"{latest.get('return_on_equity_pct', 0):.2f}%",
        ],
        [
            "ROCE",
            f"{latest.get('return_on_capital_employed_pct', 0):.2f}%",
        ],
        [
            "Debt / Equity",
            f"{latest.get('debt_to_equity', 0):.2f}",
        ],
        [
            "FCF",
            f"{latest.get('free_cash_flow_cr', 0):,.0f}",
        ],
        [
            "Revenue CAGR",
            f"{latest.get('revenue_cagr_5yr', 0):.2f}%",
        ],
        [
            "Composite Score",
            f"{latest.get('composite_quality_score', 0):.1f}",
        ],
    ]

    table = Table(
        data,
        colWidths=[2.7 * inch, 2.7 * inch],
    )

    table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EAF2FF")),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ]
        )
    )

    return table


# =====================================================
# HEADER
# =====================================================


def header(company):

    style = styles["Title"]

    style.alignment = TA_CENTER

    return Paragraph(
        f"{company['company_name']}<br/><font size=12>{company['id']}</font>",
        style,
    )


# =====================================================
# PAGE 1
# =====================================================


def build_page_one(story, company, profit, ratios):

    story.append(header(company))

    story.append(Spacer(1, 0.25 * inch))

    story.append(kpi_table(company, ratios))

    story.append(Spacer(1, 0.30 * inch))

    revenue_chart = revenue_profit_chart(
        profit,
        company["id"],
    )

    roe_chart = roe_roce_chart(
        ratios,
        company["id"],
    )

    chart_table = Table(
        [
            [
                Image(
                    str(revenue_chart),
                    width=3.2 * inch,
                    height=2.2 * inch,
                ),
                Image(
                    str(roe_chart),
                    width=3.2 * inch,
                    height=2.2 * inch,
                ),
            ]
        ]
    )

    chart_table.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )

    story.append(chart_table)

    story.append(PageBreak())


# =====================================================
# CAPITAL ALLOCATION BADGE
# =====================================================


def capital_badge(ratios):

    latest = ratios.iloc[-1]

    pattern = latest.get(
        "capital_allocation_pattern",
        "Unknown",
    )

    color = colors.grey

    if pattern == "Reinvestor":
        color = colors.green

    elif pattern == "Debt Reduction":
        color = colors.blue

    elif pattern == "Dividend":
        color = colors.orange

    elif pattern == "Distress":
        color = colors.red

    table = Table([[pattern]])

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), color),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    return table


# =====================================================
# PROS & CONS
# =====================================================


def pros_cons_table(df):

    pros = df[df["type"] == "pro"]

    cons = df[df["type"] == "con"]

    pro_text = "<br/>".join(["• " + p for p in pros["text"].head(5)])

    con_text = "<br/>".join(["• " + c for c in cons["text"].head(5)])

    style = styles["BodyText"]

    return Table(
        [
            [
                Paragraph(
                    "<b>Pros</b><br/><br/>" + pro_text,
                    style,
                ),
                Paragraph(
                    "<b>Cons</b><br/><br/>" + con_text,
                    style,
                ),
            ]
        ],
        colWidths=[
            3.3 * inch,
            3.3 * inch,
        ],
    )


# =====================================================
# PAGE 2
# =====================================================


def build_page_two(
    story,
    company,
    balance,
    cash,
    ratios,
    proscons,
):

    balance_img = balance_chart(
        balance,
        company["id"],
    )

    cash_img = cashflow_chart(
        cash,
        company["id"],
    )

    charts = Table(
        [
            [
                Image(
                    str(balance_img),
                    width=3.2 * inch,
                    height=2.2 * inch,
                ),
                Image(
                    str(cash_img),
                    width=3.2 * inch,
                    height=2.2 * inch,
                ),
            ]
        ]
    )

    charts.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ]
        )
    )

    story.append(charts)

    story.append(Spacer(1, 0.25 * inch))

    story.append(capital_badge(ratios))

    story.append(Spacer(1, 0.20 * inch))

    if len(proscons):
        story.append(pros_cons_table(proscons))

    else:
        story.append(
            Paragraph(
                "Pros & Cons not available.",
                styles["BodyText"],
            )
        )


# =====================================================
# GENERATE SINGLE PDF
# =====================================================


def generate_pdf(company_id):

    (
        company,
        profit,
        balance,
        cash,
        ratios,
    ) = validate(company_id)

    proscons = get_pros_cons(company_id)

    pdf_path = REPORT_DIR / f"{company_id}_tearsheet.pdf"

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=(8.27 * inch, 11.69 * inch),
        rightMargin=20,
        leftMargin=20,
        topMargin=20,
        bottomMargin=20,
    )

    story = []

    # ----------------------------
    # PAGE 1
    # ----------------------------

    build_page_one(
        story,
        company,
        profit,
        ratios,
    )

    # ----------------------------
    # PAGE 2
    # ----------------------------

    build_page_two(
        story,
        company,
        balance,
        cash,
        ratios,
        proscons,
    )

    doc.build(story)

    return pdf_path


# =====================================================
# GET ALL COMPANIES
# =====================================================


def get_company_list():

    return query(
        """
        SELECT id
        FROM companies
        ORDER BY id
        """
    )["id"].tolist()


# =====================================================
# VALIDATE DATA SUFFICIENCY
# =====================================================


def has_enough_data(company):

    profit = get_profit(company)

    balance = get_balance(company)

    cash = get_cashflow(company)

    ratios = get_ratios(company)

    if len(profit) < 3:
        return False

    if len(balance) < 3:
        return False

    if len(cash) < 3:
        return False

    if len(ratios) < 3:
        return False

    return True


# =====================================================
# WRITE SKIPPED LOG
# =====================================================


def write_skipped(skipped):

    if len(skipped) == 0:
        return

    pd.DataFrame(
        skipped,
        columns=["company_id", "reason"],
    ).to_csv(
        OUTPUT_DIR / "skipped_tearsheets.csv",
        index=False,
    )


# =====================================================
# GENERATE ALL PDFS
# =====================================================


def generate_all():

    companies = get_company_list()

    skipped = []

    success = 0

    print("=" * 60)
    print("Generating Company Tearsheets")
    print("=" * 60)

    for company in companies:
        try:
            if not has_enough_data(company):
                skipped.append(
                    (
                        company,
                        "Insufficient historical data",
                    )
                )

                continue

            generate_pdf(company)

            success += 1

            print(f"✔ {company}")

        except Exception as e:
            skipped.append(
                (
                    company,
                    str(e),
                )
            )

            print(f"✖ {company} -> {e}")

    write_skipped(skipped)

    print()
    print("=" * 60)
    print(f"Generated : {success}")
    print(f"Skipped  : {len(skipped)}")
    print("=" * 60)

    return success


# =====================================================
# CLEANUP
# =====================================================


def cleanup_charts():

    if not CHART_DIR.exists():
        return

    for file in CHART_DIR.glob("*.png"):
        try:
            file.unlink()

        except Exception:
            pass


# =====================================================
# SUMMARY
# =====================================================


def print_summary():

    pdfs = list(REPORT_DIR.glob("*.pdf"))

    print()
    print("=" * 60)
    print("REPORT GENERATION COMPLETE")
    print("=" * 60)
    print(f"PDFs Generated : {len(pdfs)}")
    print(f"Location       : {REPORT_DIR}")

    skipped = OUTPUT_DIR / "skipped_tearsheets.csv"

    if skipped.exists():
        print(f"Skipped Log    : {skipped}")

    print("=" * 60)


# =====================================================
# MAIN
# =====================================================


def main():

    print()
    print("=" * 60)
    print("NIFTY100 TEARSHEET GENERATOR")
    print("=" * 60)

    cleanup_charts()

    generate_all()

    cleanup_charts()

    print_summary()


# =====================================================
# ENTRY
# =====================================================

if __name__ == "__main__":
    main()
