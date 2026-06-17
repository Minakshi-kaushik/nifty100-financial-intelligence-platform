import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd

from src.etl.normaliser import normalize_ticker, normalize_year


# ==================================================
# TICKER TESTS (15)
# ==================================================


def test_ticker_uppercase():
    assert normalize_ticker("ABB") == "ABB"


def test_ticker_lowercase():
    assert normalize_ticker("abb") == "ABB"


def test_ticker_mixedcase():
    assert normalize_ticker("Abb") == "ABB"


def test_ticker_mixedcase_2():
    assert normalize_ticker("aBb") == "ABB"


def test_ticker_leading_space():
    assert normalize_ticker(" ABB") == "ABB"


def test_ticker_trailing_space():
    assert normalize_ticker("ABB ") == "ABB"


def test_ticker_both_spaces():
    assert normalize_ticker(" ABB ") == "ABB"


def test_ticker_hdfcbank():
    assert normalize_ticker("HdfcBank") == "HDFCBANK"


def test_ticker_reliance():
    assert normalize_ticker("reliance") == "RELIANCE"


def test_ticker_numeric_string():
    assert normalize_ticker("123") == "123"


def test_ticker_integer():
    assert normalize_ticker(123) == "123"


def test_ticker_none():
    assert normalize_ticker(None) is None


def test_ticker_nan():
    assert normalize_ticker(pd.NA) is None


def test_ticker_empty_string():
    assert normalize_ticker("") == ""


def test_ticker_special_char():
    assert normalize_ticker("tcs-ltd") == "TCS-LTD"


# ==================================================
# YEAR TESTS (20)
# ==================================================


def test_year_plain_2024():
    assert normalize_year("2024") == "2024"


def test_year_plain_2023():
    assert normalize_year("2023") == "2023"


def test_year_plain_2019():
    assert normalize_year("2019") == "2019"


def test_year_mar_2014():
    assert normalize_year("Mar 2014") == "2014-03"


def test_year_mar_2015():
    assert normalize_year("Mar 2015") == "2015-03"


def test_year_dec_2012():
    assert normalize_year("Dec 2012") == "2012-12"


def test_year_dec_2013():
    assert normalize_year("Dec 2013") == "2013-12"


def test_year_mar_13():
    assert normalize_year("Mar-13") == "2013-03"


def test_year_mar_14():
    assert normalize_year("Mar-14") == "2014-03"


def test_year_mar_15():
    assert normalize_year("Mar-15") == "2015-03"


def test_year_dec_16():
    assert normalize_year("Dec-16") == "2016-12"


def test_year_jan_20():
    assert normalize_year("Jan-20") == "2020-01"


def test_year_feb_21():
    assert normalize_year("Feb-21") == "2021-02"


def test_year_apr_22():
    assert normalize_year("Apr-22") == "2022-04"


def test_year_none():
    assert normalize_year(None) is None


def test_year_nan():
    assert normalize_year(pd.NA) is None


def test_year_invalid():
    assert normalize_year("invalid") is None


def test_year_random_text():
    assert normalize_year("abcd") is None


def test_year_empty():
    assert normalize_year("") is None


def test_year_wrong_format():
    assert normalize_year("2024-03") is None
