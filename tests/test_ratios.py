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
)

# ============================================================
# Day 08 Tests
# ============================================================


def test_net_profit_margin_normal():
    assert net_profit_margin(100, 1000) == 10.0


def test_net_profit_margin_zero_sales():
    assert net_profit_margin(100, 0) is None


def test_operating_profit_margin_normal():
    assert operating_profit_margin(operating_profit=250, sales=1000) == 25.0


def test_operating_profit_margin_zero_sales():
    assert operating_profit_margin(operating_profit=250, sales=0) is None


def test_return_on_equity_normal():
    assert return_on_equity(net_profit=150, equity_capital=100, reserves=400) == 30.0


def test_return_on_equity_negative_equity():
    assert return_on_equity(net_profit=100, equity_capital=-200, reserves=100) is None


def test_return_on_capital_employed():
    assert (
        return_on_capital_employed(
            operating_profit=250,
            other_income=50,
            equity_capital=100,
            reserves=400,
            borrowings=500,
        )
        == 30.0
    )


def test_return_on_assets_zero_assets():
    assert return_on_assets(net_profit=100, total_assets=0) is None


# ============================================================
# Day 09 Tests
# ============================================================


def test_debt_to_equity_normal():
    assert debt_to_equity(borrowings=500, equity_capital=100, reserves=400) == 1.0


def test_debt_to_equity_debt_free():
    assert debt_to_equity(borrowings=0, equity_capital=100, reserves=400) == 0.0


def test_high_leverage_flag():
    assert (
        high_leverage_flag(
            debt_to_equity_ratio=6, broad_sector="Information Technology"
        )
        is True
    )


def test_high_leverage_financials():
    assert (
        high_leverage_flag(debt_to_equity_ratio=8, broad_sector="Financials") is False
    )


def test_interest_coverage_ratio():
    assert (
        interest_coverage_ratio(operating_profit=300, other_income=50, interest=50)
        == 7.0
    )


def test_interest_coverage_none():
    assert (
        interest_coverage_ratio(operating_profit=300, other_income=50, interest=0)
        is None
    )


def test_icr_label():
    assert icr_label(None) == "Debt Free"


def test_icr_warning():
    assert icr_warning_flag(1.2) is True


def test_net_debt():
    assert net_debt(borrowings=500, investments=150) == 350


def test_asset_turnover():
    assert asset_turnover(sales=1000, total_assets=500) == 2.0
