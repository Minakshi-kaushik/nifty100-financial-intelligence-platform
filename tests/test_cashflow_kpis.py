import pytest

from src.analytics.cashflow_kpis import (
    free_cash_flow,
    cfo_quality_score,
    capex_intensity,
    fcf_conversion_rate,
    capital_allocation_pattern,
)


# ============================================================
# Free Cash Flow
# ============================================================


def test_free_cash_flow():
    assert free_cash_flow(500, -200) == 300


# ============================================================
# CFO Quality Score
# ============================================================


def test_cfo_quality_high():
    avg, label = cfo_quality_score(
        [100, 120, 140],
        [80, 100, 120],
    )

    assert label == "High Quality"


def test_cfo_quality_moderate():
    avg, label = cfo_quality_score(
        [60, 70, 80],
        [100, 100, 100],
    )

    assert label == "Moderate"


def test_cfo_quality_accrual():
    avg, label = cfo_quality_score(
        [20, 30, 40],
        [100, 100, 100],
    )

    assert label == "Accrual Risk"


# ============================================================
# CapEx Intensity
# ============================================================


def test_capex_asset_light():
    pct, label = capex_intensity(-20, 1000)

    assert label == "Asset Light"


def test_capex_moderate():
    pct, label = capex_intensity(-50, 1000)

    assert label == "Moderate"


def test_capex_capital_intensive():
    pct, label = capex_intensity(-150, 1000)

    assert label == "Capital Intensive"


# ============================================================
# FCF Conversion
# ============================================================


def test_fcf_conversion():
    assert fcf_conversion_rate(300, 400) == 75.0


# ============================================================
# Capital Allocation
# ============================================================


def test_capital_allocation_shareholder():
    assert (
        capital_allocation_pattern(
            500,
            -100,
            -50,
            1.2,
        )
        == "Shareholder Returns"
    )


def test_capital_allocation_growth_debt():
    assert (
        capital_allocation_pattern(
            -100,
            -50,
            200,
        )
        == "Growth Funded by Debt"
    )
