"""
portfolio_summary.py

Generates a portfolio summary PDF
with one page per company.
"""

from pathlib import Path
import sqlite3

import pandas as pd

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    PageBreak,
    Table,
    TableStyle,
)

# =====================================================
# PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "db" / "nifty100.db"

REPORT_DIR = BASE_DIR / "reports" / "portfolio"

REPORT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

OUTPUT_FILE = REPORT_DIR / "portfolio_summary.pdf"

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
# LOAD DATA
# =====================================================


def load_portfolio():

    sql = """
    SELECT

        c.id,

        c.company_name,

        s.broad_sector,

        fr.return_on_equity_pct,

        fr.return_on_capital_employed_pct,

        fr.debt_to_equity,

        fr.free_cash_flow_cr,

        fr.composite_quality_score,

        fr.capital_allocation_pattern,

        mc.pe_ratio,

        mc.pb_ratio

    FROM companies c

    LEFT JOIN sectors s
        ON c.id=s.company_id

    LEFT JOIN financial_ratios fr
        ON c.id=fr.company_id

    LEFT JOIN market_cap mc
        ON c.id=mc.company_id

    WHERE fr.year='Mar 2024'

    AND mc.year=2024

    ORDER BY c.company_name
    """

    return query(sql)


# =====================================================
# KPI TABLE
# =====================================================


def build_kpi_table(company):

    data = [
        ["Sector", company["broad_sector"]],
        [
            "ROE (%)",
            f"{company['return_on_equity_pct']:.2f}"
            if pd.notna(company["return_on_equity_pct"])
            else "-",
        ],
        [
            "ROCE (%)",
            f"{company['return_on_capital_employed_pct']:.2f}"
            if pd.notna(company["return_on_capital_employed_pct"])
            else "-",
        ],
        [
            "Debt / Equity",
            f"{company['debt_to_equity']:.2f}"
            if pd.notna(company["debt_to_equity"])
            else "-",
        ],
        [
            "PE Ratio",
            f"{company['pe_ratio']:.2f}" if pd.notna(company["pe_ratio"]) else "-",
        ],
        [
            "PB Ratio",
            f"{company['pb_ratio']:.2f}" if pd.notna(company["pb_ratio"]) else "-",
        ],
        [
            "Free Cash Flow",
            f"{company['free_cash_flow_cr']:,.0f}"
            if pd.notna(company["free_cash_flow_cr"])
            else "-",
        ],
        [
            "Composite Score",
            f"{company['composite_quality_score']:.1f}"
            if pd.notna(company["composite_quality_score"])
            else "-",
        ],
        [
            "Capital Allocation",
            company["capital_allocation_pattern"]
            if pd.notna(company["capital_allocation_pattern"])
            else "-",
        ],
    ]

    table = Table(
        data,
        colWidths=[2.7 * inch, 3.5 * inch],
    )

    table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#E8F0FE")),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ]
        )
    )

    return table


# =====================================================
# TREND ARROW
# =====================================================


def trend_arrow(value):

    if pd.isna(value):
        return "→"

    if value >= 20:
        return "↑"

    if value >= 10:
        return "→"

    return "↓"


# =====================================================
# COMPANY PAGE
# =====================================================


def company_page(story, company):

    title = Paragraph(
        f"<b><font size=20>{company['company_name']}</font></b><br/>"
        f"<font size=12>{company['id']}</font>",
        styles["Title"],
    )

    story.append(title)

    story.append(Spacer(1, 0.25 * inch))

    story.append(build_kpi_table(company))

    story.append(Spacer(1, 0.30 * inch))

    roe_arrow = trend_arrow(company["return_on_equity_pct"])

    roce_arrow = trend_arrow(company["return_on_capital_employed_pct"])

    score_arrow = trend_arrow(company["composite_quality_score"])

    summary = f"""
    <b>Performance Summary</b><br/><br/>

    ROE Trend : {roe_arrow}<br/>

    ROCE Trend : {roce_arrow}<br/>

    Composite Score : {score_arrow}<br/>

    Sector : {company["broad_sector"]}<br/>

    Capital Allocation :
    {company["capital_allocation_pattern"]}
    """

    story.append(
        Paragraph(
            summary,
            styles["BodyText"],
        )
    )

    story.append(PageBreak())


# =====================================================
# BUILD PDF
# =====================================================


def build_pdf():

    df = load_portfolio()

    if df.empty:
        print("No data found.")

        return

    doc = SimpleDocTemplate(
        str(OUTPUT_FILE),
        pagesize=(8.27 * inch, 11.69 * inch),
    )

    story = []

    # ---------------- Cover Page ---------------- #

    story.append(
        Paragraph(
            "<b><font size=24>NIFTY 100 Portfolio Summary</font></b>",
            styles["Title"],
        )
    )

    story.append(Spacer(1, 0.40 * inch))

    story.append(
        Paragraph(
            f"Total Companies : <b>{len(df)}</b>",
            styles["Heading2"],
        )
    )

    story.append(Spacer(1, 0.20 * inch))

    story.append(
        Paragraph(
            """
            This report summarizes the latest financial
            performance, valuation and capital allocation
            metrics for companies in the NIFTY100 universe.
            """,
            styles["BodyText"],
        )
    )

    story.append(PageBreak())

    # ---------------- Company Pages ---------------- #

    for _, company in df.iterrows():
        company_page(
            story,
            company,
        )

    doc.build(story)

    print("=" * 60)
    print("PORTFOLIO SUMMARY GENERATED")
    print("=" * 60)
    print(OUTPUT_FILE)
    print("=" * 60)


# =====================================================
# MAIN
# =====================================================


def main():

    build_pdf()


# =====================================================
# ENTRY POINT
# =====================================================

if __name__ == "__main__":
    main()
