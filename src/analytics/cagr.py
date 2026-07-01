"""
cagr.py

Sprint 2 - CAGR Engine

Implements CAGR calculations for:
- Revenue
- PAT
- EPS

Handles all required Sprint 2 edge cases.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional


# ============================================================
# CAGR Status Flags
# ============================================================


class CAGRFlag(str, Enum):
    NORMAL = "NORMAL"
    TURNAROUND = "TURNAROUND"
    DECLINE_TO_LOSS = "DECLINE_TO_LOSS"
    BOTH_NEGATIVE = "BOTH_NEGATIVE"
    ZERO_BASE = "ZERO_BASE"
    INSUFFICIENT = "INSUFFICIENT"


# ============================================================
# CAGR Calculation
# ============================================================


def calculate_cagr(
    start_value: float,
    end_value: float,
    years: int,
) -> tuple[Optional[float], CAGRFlag]:
    """
    Calculates CAGR.

    Returns:
        (value, flag)
    """

    if years <= 0:
        return None, CAGRFlag.INSUFFICIENT

    if start_value == 0:
        return None, CAGRFlag.ZERO_BASE

    if start_value > 0 and end_value < 0:
        return None, CAGRFlag.DECLINE_TO_LOSS

    if start_value < 0 and end_value > 0:
        return None, CAGRFlag.TURNAROUND

    if start_value < 0 and end_value < 0:
        return None, CAGRFlag.BOTH_NEGATIVE

    value = ((end_value / start_value) ** (1 / years) - 1) * 100

    return round(value, 2), CAGRFlag.NORMAL


# ============================================================
# Revenue CAGR
# ============================================================


def revenue_cagr(
    start_sales: float,
    end_sales: float,
    years: int,
):
    return calculate_cagr(
        start_sales,
        end_sales,
        years,
    )


# ============================================================
# PAT CAGR
# ============================================================


def pat_cagr(
    start_profit: float,
    end_profit: float,
    years: int,
):
    return calculate_cagr(
        start_profit,
        end_profit,
        years,
    )


# ============================================================
# EPS CAGR
# ============================================================


def eps_cagr(
    start_eps: float,
    end_eps: float,
    years: int,
):
    return calculate_cagr(
        start_eps,
        end_eps,
        years,
    )


# ============================================================
# Historical Window Helpers
# ============================================================


def revenue_cagr_3yr(start_sales: float, end_sales: float):
    return revenue_cagr(start_sales, end_sales, 3)


def revenue_cagr_5yr(start_sales: float, end_sales: float):
    return revenue_cagr(start_sales, end_sales, 5)


def revenue_cagr_10yr(start_sales: float, end_sales: float):
    return revenue_cagr(start_sales, end_sales, 10)


def pat_cagr_3yr(start_profit: float, end_profit: float):
    return pat_cagr(start_profit, end_profit, 3)


def pat_cagr_5yr(start_profit: float, end_profit: float):
    return pat_cagr(start_profit, end_profit, 5)


def pat_cagr_10yr(start_profit: float, end_profit: float):
    return pat_cagr(start_profit, end_profit, 10)


def eps_cagr_3yr(start_eps: float, end_eps: float):
    return eps_cagr(start_eps, end_eps, 3)


def eps_cagr_5yr(start_eps: float, end_eps: float):
    return eps_cagr(start_eps, end_eps, 5)


def eps_cagr_10yr(start_eps: float, end_eps: float):
    return eps_cagr(start_eps, end_eps, 10)


# ============================================================
# Generic History Helper
# ============================================================


def calculate_metric_cagr(
    history: list[float],
    years: int,
):
    """
    history

    Example

    [120,140,170,200,250,310]

    Oldest ----------> Latest
    """

    if len(history) <= years:
        return None, CAGRFlag.INSUFFICIENT

    start = history[-(years + 1)]
    end = history[-1]

    return calculate_cagr(
        start,
        end,
        years,
    )


if __name__ == "__main__":
    value, flag = revenue_cagr(
        100,
        200,
        5,
    )

    print(f"CAGR : {value}")
    print(f"Flag : {flag}")
