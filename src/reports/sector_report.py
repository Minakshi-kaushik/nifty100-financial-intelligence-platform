"""
sector_report.py

Generates one PDF report for every sector.
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
    Table,
    TableStyle,
)

# =====================================================
# PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "db" / "nifty100.db"

REPORT_DIR = BASE_DIR / "reports" / "sector"

REPORT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

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
# GET SECTOR LIST
# =====================================================


def get_sectors():

    return query(
        """
        SELECT DISTINCT broad_sector
        FROM sectors
        ORDER BY broad_sector
        """
    )["broad_sector"].tolist()


# =====================================================
# GET SECTOR DATA
# =====================================================


def get_sector_data(sector):

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

        mc.pe_ratio,

        mc.pb_ratio,

        mc.ev_ebitda

    FROM companies c

    JOIN sectors s
        ON c.id=s.company_id

    LEFT JOIN financial_ratios fr
        ON c.id=fr.company_id

    LEFT JOIN market_cap mc
        ON c.id=mc.company_id

    WHERE s.broad_sector=?

    AND fr.year='Mar 2024'

    AND mc.year=2024

    ORDER BY c.company_name
    """

    return query(
        sql,
        [sector],
    )


# =====================================================
# SUMMARY TABLE
# =====================================================


def sector_summary(df):

    summary = [
        [
            "Companies",
            len(df),
        ],
        [
            "Median ROE",
            round(
                df["return_on_equity_pct"].median(),
                2,
            ),
        ],
        [
            "Median ROCE",
            round(
                df["return_on_capital_employed_pct"].median(),
                2,
            ),
        ],
        [
            "Median PE",
            round(
                df["pe_ratio"].median(),
                2,
            ),
        ],
        [
            "Median PB",
            round(
                df["pb_ratio"].median(),
                2,
            ),
        ],
        [
            "Median D/E",
            round(
                df["debt_to_equity"].median(),
                2,
            ),
        ],
    ]

    table = Table(
        summary,
        colWidths=[3 * inch, 2 * inch],
    )

    table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#E8F0FE")),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    return table


# =====================================================
# COMPANY COMPARISON TABLE
# =====================================================


def company_table(df):

    columns = [
        "company_name",
        "return_on_equity_pct",
        "return_on_capital_employed_pct",
        "debt_to_equity",
        "pe_ratio",
        "pb_ratio",
        "free_cash_flow_cr",
        "composite_quality_score",
    ]

    table_data = [
        [
            "Company",
            "ROE",
            "ROCE",
            "D/E",
            "PE",
            "PB",
            "FCF",
            "Score",
        ]
    ]

    for _, row in df.iterrows():
        table_data.append(
            [
                row["company_name"],
                f"{row['return_on_equity_pct']:.2f}"
                if pd.notna(row["return_on_equity_pct"])
                else "-",
                f"{row['return_on_capital_employed_pct']:.2f}"
                if pd.notna(row["return_on_capital_employed_pct"])
                else "-",
                f"{row['debt_to_equity']:.2f}"
                if pd.notna(row["debt_to_equity"])
                else "-",
                f"{row['pe_ratio']:.2f}" if pd.notna(row["pe_ratio"]) else "-",
                f"{row['pb_ratio']:.2f}" if pd.notna(row["pb_ratio"]) else "-",
                f"{row['free_cash_flow_cr']:,.0f}"
                if pd.notna(row["free_cash_flow_cr"])
                else "-",
                f"{row['composite_quality_score']:.1f}"
                if pd.notna(row["composite_quality_score"])
                else "-",
            ]
        )

    table = Table(
        table_data,
        repeatRows=1,
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("TOPPADDING", (0, 1), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
            ]
        )
    )

    return table


# =====================================================
# BUILD PDF
# =====================================================


def generate_sector_pdf(sector):

    df = get_sector_data(sector)

    if df.empty:
        print(f"Skipping {sector} (No data)")

        return

    pdf = REPORT_DIR / f"{sector}_report.pdf"

    doc = SimpleDocTemplate(
        str(pdf),
        pagesize=(8.27 * inch, 11.69 * inch),
    )

    story = []

    title = Paragraph(
        f"<b><font size=20>{sector} Sector Report</font></b>",
        styles["Title"],
    )

    story.append(title)

    story.append(Spacer(1, 0.30 * inch))

    story.append(
        Paragraph(
            f"Total Companies : <b>{len(df)}</b>",
            styles["BodyText"],
        )
    )

    story.append(Spacer(1, 0.20 * inch))

    story.append(sector_summary(df))

    story.append(Spacer(1, 0.30 * inch))

    story.append(
        Paragraph(
            "<b>Company Comparison</b>",
            styles["Heading2"],
        )
    )

    story.append(Spacer(1, 0.10 * inch))

    story.append(company_table(df))

    doc.build(story)

    print(f"Generated : {sector}")


# =====================================================
# GENERATE ALL SECTOR REPORTS
# =====================================================


def generate_all():

    sectors = get_sectors()

    generated = 0

    skipped = 0

    print("=" * 60)
    print("Generating Sector Reports")
    print("=" * 60)

    for sector in sectors:
        try:
            generate_sector_pdf(sector)

            generated += 1

        except Exception as e:
            skipped += 1

            print(f"{sector} -> {e}")

    print()

    print("=" * 60)
    print("SECTOR REPORT SUMMARY")
    print("=" * 60)

    print(f"Generated : {generated}")

    print(f"Skipped   : {skipped}")

    print(f"Output    : {REPORT_DIR}")

    print("=" * 60)


# =====================================================
# MAIN
# =====================================================


def main():

    generate_all()


# =====================================================
# ENTRY POINT
# =====================================================

if __name__ == "__main__":
    main()
