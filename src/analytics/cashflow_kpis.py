"""
cashflow_kpis.py

Sprint 2 - Cash Flow KPI Engine

Implements:
- Free Cash Flow
- CFO Quality Score
- CapEx Intensity
- FCF Conversion Rate
- Capital Allocation Pattern Classification
"""

from __future__ import annotations

from typing import Optional


# ============================================================
# Helper
# ============================================================


def safe_round(value: Optional[float], digits: int = 2):
    if value is None:
        return None

    return round(value, digits)


# ============================================================
# Free Cash Flow
# ============================================================


def free_cash_flow(
    operating_activity,
    investing_activity,
):
    if operating_activity is None or investing_activity is None:
        return None

    return safe_round(operating_activity + investing_activity)


# ============================================================
# CFO Quality Score
# ============================================================


def cfo_quality_score(
    cfo_values: list[float],
    pat_values: list[float],
):
    """
    Average CFO/PAT ratio across available years.

    >1.0 High Quality
    0.5-1.0 Moderate
    <0.5 Accrual Risk
    """

    if len(cfo_values) != len(pat_values):
        raise ValueError("History length mismatch")

    ratios = []

    for cfo, pat in zip(cfo_values, pat_values):
        if pat == 0:
            continue

        ratios.append(cfo / pat)

    if not ratios:
        return None

    avg = sum(ratios) / len(ratios)

    avg = safe_round(avg)

    if avg > 1:
        return avg, "High Quality"

    if avg >= 0.5:
        return avg, "Moderate"

    return avg, "Accrual Risk"


# ============================================================
# CapEx Intensity
# ============================================================


def capex_intensity(
    investing_activity: float,
    sales: float,
):
    """
    CapEx Intensity

    abs(CapEx) / Sales
    """

    if sales == 0:
        return None

    pct = abs(investing_activity) / sales * 100

    pct = safe_round(pct)

    if pct < 3:
        label = "Asset Light"

    elif pct <= 8:
        label = "Moderate"

    else:
        label = "Capital Intensive"

    return pct, label


# ============================================================
# FCF Conversion
# ============================================================


def fcf_conversion_rate(
    free_cash_flow_value: float,
    operating_profit: float,
):
    """
    FCF / Operating Profit
    """

    if operating_profit == 0:
        return None

    return safe_round(free_cash_flow_value / operating_profit * 100)


# ============================================================
# Capital Allocation Pattern
# ============================================================


def capital_allocation_pattern(
    operating_activity: float,
    investing_activity: float,
    financing_activity: float,
    cfo_pat_ratio: Optional[float] = None,
):
    """
    Classify capital allocation pattern.
    """

    cfo = operating_activity >= 0
    cfi = investing_activity >= 0
    cff = financing_activity >= 0

    pattern = (cfo, cfi, cff)

    if pattern == (True, False, False):
        if cfo_pat_ratio is not None and cfo_pat_ratio > 1:
            return "Shareholder Returns"

        return "Reinvestor"

    if pattern == (True, True, False):
        return "Liquidating Assets"

    if pattern == (False, True, True):
        return "Distress Signal"

    if pattern == (False, False, True):
        return "Growth Funded by Debt"

    if pattern == (True, True, True):
        return "Cash Accumulator"

    if pattern == (False, False, False):
        return "Pre-Revenue"

    if pattern == (True, False, True):
        return "Mixed"

    return "Unknown"


if __name__ == "__main__":
    fcf = free_cash_flow(
        500,
        -200,
    )

    print("FCF :", fcf)

    print(
        cfo_quality_score(
            [100, 120, 130, 140, 150],
            [90, 100, 120, 130, 140],
        )
    )

    print(
        capex_intensity(
            -50,
            1000,
        )
    )

    print(
        fcf_conversion_rate(
            fcf,
            400,
        )
    )

    print(
        capital_allocation_pattern(
            400,
            -150,
            -100,
            1.2,
        )
    )


def calculate_cashflow_kpis(
    *,
    operating_activity: float,
    investing_activity: float,
    financing_activity: float,
    operating_profit: float,
    sales: float,
    cfo_history: list[float],
    pat_history: list[float],
):
    """
    Calculate all cash flow KPIs for a company-year.
    """

    fcf = free_cash_flow(
        operating_activity,
        investing_activity,
    )

    quality = cfo_quality_score(
        cfo_history,
        pat_history,
    )

    if quality is None:
        score = None
        quality_label = None
        ratio = None
    else:
        score, quality_label = quality
        ratio = score

    capex = capex_intensity(
        investing_activity,
        sales,
    )

    if capex is None:
        capex_pct = None
        capex_label = None
    else:
        capex_pct, capex_label = capex

    return {
        "free_cash_flow_cr": fcf,
        "cfo_quality_score": score,
        "cfo_quality_label": quality_label,
        "capex_cr": capex_pct,
        "capex_label": capex_label,
        "fcf_conversion_pct": fcf_conversion_rate(
            fcf,
            operating_profit,
        ),
        "capital_allocation_pattern": capital_allocation_pattern(
            operating_activity,
            investing_activity,
            financing_activity,
            ratio,
        ),
    }
