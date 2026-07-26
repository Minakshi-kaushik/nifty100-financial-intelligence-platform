import pytest

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
    debt_to_equity,
    high_leverage_flag,
    interest_coverage_ratio,
    icr_label,
    icr_warning_flag,
    net_debt,
    asset_turnover,
    calculate_ratios,
)


# ===========================================================
# Net Profit Margin
# ===========================================================


def test_net_profit_margin():
    assert net_profit_margin(100, 1000) == 10.0


def test_net_profit_margin_zero_sales():
    assert net_profit_margin(100, 0) is None


# ===========================================================
# Operating Profit Margin
# ===========================================================


def test_operating_profit_margin():
    assert operating_profit_margin(250, 1000) == 25.0


def test_operating_profit_margin_zero_sales():
    assert operating_profit_margin(250, 0) is None


# ===========================================================
# Return on Equity
# ===========================================================


def test_return_on_equity():
    assert return_on_equity(100, 100, 400) == 20.0


def test_return_on_equity_negative_equity():
    assert return_on_equity(100, -100, 50) is None


# ===========================================================
# Return on Capital Employed
# ===========================================================


def test_roce():
    assert (
        return_on_capital_employed(
            200,
            20,
            100,
            400,
            500,
        )
        == 22.0
    )


def test_roce_invalid_capital():
    assert (
        return_on_capital_employed(
            200,
            20,
            0,
            0,
            0,
        )
        is None
    )


# ===========================================================
# Return on Assets
# ===========================================================


def test_roa():
    assert return_on_assets(100, 1000) == 10.0


def test_roa_invalid_assets():
    assert return_on_assets(100, 0) is None


# ===========================================================
# Debt to Equity
# ===========================================================


def test_debt_to_equity():
    assert debt_to_equity(500, 100, 400) == 1.0


def test_debt_free_company():
    assert debt_to_equity(0, 100, 400) == 0.0


def test_debt_to_equity_negative_equity():
    assert debt_to_equity(100, -50, 20) is None


# ===========================================================
# High Leverage
# ===========================================================


def test_high_leverage_true():
    assert high_leverage_flag(6.2, "Information Technology")


def test_high_leverage_financial():
    assert not high_leverage_flag(10, "Financials")


# ===========================================================
# Interest Coverage
# ===========================================================


def test_interest_coverage():
    assert (
        interest_coverage_ratio(
            200,
            20,
            20,
        )
        == 11.0
    )


def test_interest_zero():
    assert (
        interest_coverage_ratio(
            200,
            20,
            0,
        )
        is None
    )


# ===========================================================
# ICR Labels
# ===========================================================


def test_icr_label():
    assert icr_label(None) == "Debt Free"


def test_icr_warning():
    assert icr_warning_flag(1.2)


def test_icr_warning_false():
    assert not icr_warning_flag(3.5)


# ===========================================================
# Net Debt
# ===========================================================


def test_net_debt():
    assert net_debt(500, 100) == 400


# ===========================================================
# Asset Turnover
# ===========================================================


def test_asset_turnover():
    assert asset_turnover(1000, 500) == 2.0


def test_asset_turnover_zero_assets():
    assert asset_turnover(1000, 0) is None


# ===========================================================
# Complete Ratio Engine
# ===========================================================


def test_calculate_ratios():

    ratios = calculate_ratios(
        company="ABC",
        year="2024",
        sales=1000,
        net_profit=100,
        operating_profit=200,
        other_income=20,
        interest=20,
        opm_percentage=20,
        equity_capital=100,
        reserves=400,
        borrowings=500,
        investments=100,
        total_assets=1200,
        broad_sector="Information Technology",
    )

    assert isinstance(ratios, dict)

    assert "return_on_equity_pct" in ratios

    assert "debt_to_equity" in ratios

    assert "interest_coverage" in ratios

    assert "asset_turnover" in ratios
