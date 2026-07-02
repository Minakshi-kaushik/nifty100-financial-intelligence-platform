"""
ratios.py

Sprint 2 - Financial Ratio Engine

This module implements profitability ratios used throughout the
NIFTY100 Financial Analytics Platform.

Implemented:
---------------
✓ Net Profit Margin
✓ Operating Profit Margin
✓ OPM Validation

Author: Sprint 2
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional


# ============================================================
# Logging Configuration
# ============================================================

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "ratio_edge_cases.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


# ============================================================
# Helper Function
# ============================================================


def safe_round(value: Optional[float], digits: int = 2) -> Optional[float]:
    """
    Safely round a floating point number.

    Parameters
    ----------
    value : float | None

    digits : int

    Returns
    -------
    float | None
    """

    if value is None:
        return None

    return round(value, digits)


# ============================================================
# Net Profit Margin
# ============================================================


def net_profit_margin(net_profit: float, sales: float) -> Optional[float]:
    """
    Net Profit Margin

    Formula

        Net Profit / Sales × 100

    Returns None if Sales == 0.
    """

    if sales == 0:
        return None

    ratio = (net_profit / sales) * 100

    return safe_round(ratio)


# ============================================================
# Operating Profit Margin
# ============================================================


def operating_profit_margin(
    operating_profit: float,
    sales: float,
    source_opm: Optional[float] = None,
    company: str = "",
    year: str = "",
) -> Optional[float]:
    """
    Operating Profit Margin

    Formula

        Operating Profit / Sales ×100

    Parameters
    ----------
    operating_profit

    sales

    source_opm
        Existing OPM present in dataset

    company

    year

    Returns
    -------
    float | None
    """

    if sales == 0:
        return None

    calculated = (operating_profit / sales) * 100

    calculated = safe_round(calculated)

    # ----------------------------------------
    # Cross-check against source OPM
    # ----------------------------------------

    if source_opm is not None:
        difference = abs(calculated - source_opm)

        if difference > 1:
            logger.warning(
                (
                    f"OPM mismatch | "
                    f"Company={company} | "
                    f"Year={year} | "
                    f"Calculated={calculated:.2f}% | "
                    f"Source={source_opm:.2f}% | "
                    f"Difference={difference:.2f}%"
                )
            )

    return calculated


# ============================================================
# Return on Equity (ROE)
# ============================================================


def return_on_equity(
    net_profit: float, equity_capital: float, reserves: float
) -> Optional[float]:
    """
    Return on Equity (ROE)

    Formula:
        Net Profit / (Equity Capital + Reserves) × 100

    Returns
    -------
    float | None
        None if equity + reserves <= 0
    """

    total_equity = equity_capital + reserves

    if total_equity <= 0:
        return None

    roe = (net_profit / total_equity) * 100

    return safe_round(roe)


# ============================================================
# Return on Capital Employed (ROCE)
# ============================================================


def return_on_capital_employed(
    operating_profit: float,
    other_income: float,
    equity_capital: float,
    reserves: float,
    borrowings: float,
    broad_sector: str = "",
) -> Optional[float]:
    """
    Return on Capital Employed (ROCE)

    Formula:
        EBIT / (Equity + Reserves + Borrowings) × 100

    EBIT is approximated as:
        Operating Profit + Other Income

    For Financial sector companies,
    threshold checks are skipped because
    leverage is structurally different.
    """

    capital_employed = equity_capital + reserves + borrowings

    if capital_employed <= 0:
        return None

    ebit = operating_profit + other_income

    roce = (ebit / capital_employed) * 100

    roce = safe_round(roce)

    # Sector-specific handling
    if broad_sector.strip().lower() == "financials":
        logger.info(f"Financial sector company detected. ROCE benchmark skipped.")

    return roce


# ============================================================
# Return on Assets (ROA)
# ============================================================


def return_on_assets(net_profit: float, total_assets: float) -> Optional[float]:
    """
    Return on Assets (ROA)

    Formula:
        Net Profit / Total Assets × 100

    Returns None if total_assets <= 0.
    """

    if total_assets <= 0:
        return None

    roa = (net_profit / total_assets) * 100

    return safe_round(roa)


# ============================================================
# Debt to Equity Ratio
# ============================================================


def debt_to_equity(
    borrowings: float, equity_capital: float, reserves: float
) -> Optional[float]:
    """
    Debt-to-Equity Ratio

    Formula:
        Borrowings / (Equity + Reserves)

    Returns:
        0.0 if borrowings == 0
        None if equity + reserves <= 0
    """

    if borrowings == 0:
        return 0.0

    total_equity = equity_capital + reserves

    if total_equity <= 0:
        return None

    return safe_round(borrowings / total_equity)


# ============================================================
# High Leverage Flag
# ============================================================


def high_leverage_flag(
    debt_to_equity_ratio: Optional[float], broad_sector: str
) -> bool:
    """
    Returns True if:
        D/E > 5 AND company is not in Financials.
    """

    if debt_to_equity_ratio is None:
        return False

    if broad_sector.strip().lower() == "financials":
        return False

    return debt_to_equity_ratio > 5


# ============================================================
# Interest Coverage Ratio
# ============================================================


def interest_coverage_ratio(
    operating_profit,
    other_income,
    interest,
):
    """
    Interest Coverage Ratio

    EBIT / Interest
    """

    operating_profit = operating_profit or 0
    other_income = other_income or 0

    if interest in (None, 0):
        return None

    ebit = operating_profit + other_income

    return safe_round(ebit / interest)


# ============================================================
# ICR Label
# ============================================================


def icr_label(icr: Optional[float]) -> Optional[str]:
    """
    Returns:
        'Debt Free' if ICR is None.
    """

    if icr is None:
        return "Debt Free"

    return None


# ============================================================
# ICR Warning Flag
# ============================================================


def icr_warning_flag(icr: Optional[float]) -> bool:
    """
    Company at risk if ICR < 1.5.
    """

    if icr is None:
        return False

    return icr < 1.5


# ============================================================
# Net Debt
# ============================================================


def net_debt(borrowings: float, investments: float) -> float:
    """
    Net Debt

    Formula:
        Borrowings - Investments
    """

    return safe_round(borrowings - investments)


# ============================================================
# Asset Turnover
# ============================================================


def asset_turnover(sales: float, total_assets: float) -> Optional[float]:
    """
    Asset Turnover

    Formula:
        Sales / Total Assets

    Returns None if assets <= 0.
    """

    if total_assets <= 0:
        return None

    return safe_round(sales / total_assets)


# ============================================================
# Profitability Ratio Summary
# ============================================================


def calculate_ratios(
    *,
    company: str,
    year: str,
    sales: float,
    net_profit: float,
    operating_profit: float,
    other_income: float,
    interest: float,
    opm_percentage: Optional[float],
    equity_capital: float,
    reserves: float,
    borrowings: float,
    investments: float,
    total_assets: float,
    broad_sector: str,
) -> dict:
    """
    Calculate all profitability and leverage ratios
    for a company-year.

    Returns
    -------
    dict
        Dictionary containing all computed KPI values.
    """

    # Calculate reusable values
    de_ratio = debt_to_equity(
        borrowings,
        equity_capital,
        reserves,
    )

    icr = interest_coverage_ratio(
        operating_profit,
        other_income,
        interest,
    )

    return {
        # =====================================================
        # Profitability Ratios
        # =====================================================
        "net_profit_margin_pct": net_profit_margin(
            net_profit,
            sales,
        ),
        "operating_profit_margin_pct": operating_profit_margin(
            operating_profit,
            sales,
            opm_percentage,
            company,
            year,
        ),
        "return_on_equity_pct": return_on_equity(
            net_profit,
            equity_capital,
            reserves,
        ),
        "return_on_capital_employed_pct": return_on_capital_employed(
            operating_profit,
            other_income,
            equity_capital,
            reserves,
            borrowings,
            broad_sector,
        ),
        "return_on_assets_pct": return_on_assets(
            net_profit,
            total_assets,
        ),
        # =====================================================
        # Leverage & Efficiency Ratios
        # =====================================================
        "debt_to_equity": de_ratio,
        "high_leverage_flag": high_leverage_flag(
            de_ratio,
            broad_sector,
        ),
        "interest_coverage": icr,
        "icr_label": icr_label(
            icr,
        ),
        "icr_warning_flag": icr_warning_flag(
            icr,
        ),
        "net_debt": net_debt(
            borrowings,
            investments,
        ),
        "asset_turnover": asset_turnover(
            sales,
            total_assets,
        ),
    }


# ============================================================
# Demo
# ============================================================

# ============================================================
# Demo
# ============================================================

if __name__ == "__main__":
    ratios = calculate_ratios(
        company="ABC Ltd",
        year="2025",
        sales=1000,
        net_profit=120,
        operating_profit=220,
        other_income=10,
        interest=20,
        opm_percentage=22.5,
        equity_capital=100,
        reserves=500,
        borrowings=200,
        investments=50,
        total_assets=1200,
        broad_sector="Information Technology",
    )

    print("\n========== Financial Ratio Engine ==========\n")

    for key, value in ratios.items():
        print(f"{key:35} : {value}")

    print("\nFinancial Ratio Engine Loaded Successfully")
