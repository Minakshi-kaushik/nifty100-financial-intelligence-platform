import pytest

from src.etl.normaliser import (
    normalize_ticker,
    normalize_year,
)


# =====================================================
# normalize_ticker()
# =====================================================


def test_ticker_uppercase():
    assert normalize_ticker("abb") == "ABB"


def test_ticker_strip_spaces():
    assert normalize_ticker(" ABB ") == "ABB"


def test_ticker_mixed_case():
    assert normalize_ticker("HdfcBank") == "HDFCBANK"


def test_ticker_numeric():
    assert normalize_ticker(123) == "123"


def test_ticker_none():
    assert normalize_ticker(None) is None


def test_ticker_nan():
    import pandas as pd

    assert normalize_ticker(pd.NA) is None


# =====================================================
# normalize_year()
# =====================================================


def test_year_mar_2024():
    assert normalize_year("Mar 2024") == "2024-03"


def test_year_dec_2012():
    assert normalize_year("Dec 2012") == "2012-12"


def test_year_mar13():
    assert normalize_year("Mar-13") == "2013-03"


def test_year_sep19():
    assert normalize_year("Sep-19") == "2019-09"


def test_year_full_year():
    assert normalize_year("2024") == "2024"


def test_year_strip_spaces():
    assert normalize_year("  Mar 2024 ") == "2024-03"


def test_year_lowercase():
    assert normalize_year("mar 2024") == "2024-03"


def test_year_uppercase():
    assert normalize_year("MAR 2024") == "2024-03"


def test_year_invalid_month():
    assert normalize_year("Abc 2024") is None


def test_year_invalid_text():
    assert normalize_year("Hello") is None


def test_year_invalid_dash():
    assert normalize_year("2024-Mar") is None


def test_year_invalid_number():
    assert normalize_year("12345") is None


def test_year_empty():
    assert normalize_year("") is None


def test_year_none():
    assert normalize_year(None) is None


def test_year_nan():
    import pandas as pd

    assert normalize_year(pd.NA) is None


def test_year_jan():
    assert normalize_year("Jan 2020") == "2020-01"


def test_year_aug():
    assert normalize_year("Aug 2021") == "2021-08"


def test_year_oct():
    assert normalize_year("Oct-22") == "2022-10"
