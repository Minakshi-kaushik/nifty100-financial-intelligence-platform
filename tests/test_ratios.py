import pytest

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
)


# ============================================================
# Net Profit Margin
# ============================================================


def test_net_profit_margin_normal():
    assert net_profit_margin(100, 1000) == 10.0


def test_net_profit_margin_zero_sales():
    assert net_profit_margin(100, 0) is None


# ============================================================
# Operating Profit Margin
# ============================================================


def test_operating_profit_margin_normal():
    assert operating_profit_margin(operating_profit=250, sales=1000) == 25.0


def test_operating_profit_margin_zero_sales():
    assert operating_profit_margin(operating_profit=250, sales=0) is None


# ============================================================
# Return on Equity
# ============================================================


def test_return_on_equity_normal():
    assert return_on_equity(net_profit=150, equity_capital=100, reserves=400) == 30.0


def test_return_on_equity_negative_equity():
    assert return_on_equity(net_profit=100, equity_capital=-200, reserves=100) is None


# ============================================================
# Return on Capital Employed
# ============================================================


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


# ============================================================
# Return on Assets
# ============================================================


def test_return_on_assets_zero_assets():
    assert return_on_assets(net_profit=100, total_assets=0) is None
