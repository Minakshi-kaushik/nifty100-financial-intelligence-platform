import pytest

from src.analytics.cagr import (
    calculate_cagr,
    CAGRFlag,
)


def test_normal_cagr():

    value, flag = calculate_cagr(
        100,
        200,
        5,
    )

    assert flag == CAGRFlag.NORMAL
    assert round(value, 2) == 14.87


def test_zero_base():

    value, flag = calculate_cagr(
        0,
        200,
        5,
    )

    assert value is None
    assert flag == CAGRFlag.ZERO_BASE


def test_turnaround():

    value, flag = calculate_cagr(
        -100,
        200,
        5,
    )

    assert value is None
    assert flag == CAGRFlag.TURNAROUND


def test_decline_to_loss():

    value, flag = calculate_cagr(
        100,
        -20,
        5,
    )

    assert value is None
    assert flag == CAGRFlag.DECLINE_TO_LOSS


def test_both_negative():

    value, flag = calculate_cagr(
        -50,
        -10,
        5,
    )

    assert value is None
    assert flag == CAGRFlag.BOTH_NEGATIVE


def test_insufficient():

    value, flag = calculate_cagr(
        100,
        200,
        0,
    )

    assert value is None
    assert flag == CAGRFlag.INSUFFICIENT


def test_revenue_growth():

    value, flag = calculate_cagr(
        500,
        1000,
        10,
    )

    assert flag == CAGRFlag.NORMAL


def test_pat_growth():

    value, flag = calculate_cagr(
        50,
        120,
        5,
    )

    assert flag == CAGRFlag.NORMAL


def test_eps_growth():

    value, flag = calculate_cagr(
        20,
        40,
        5,
    )

    assert flag == CAGRFlag.NORMAL


def test_negative_years():

    value, flag = calculate_cagr(
        100,
        200,
        -5,
    )

    assert value is None
    assert flag == CAGRFlag.INSUFFICIENT
