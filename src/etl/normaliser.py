import re
import pandas as pd


MONTH_MAP = {
    "JAN": "01",
    "FEB": "02",
    "MAR": "03",
    "APR": "04",
    "MAY": "05",
    "JUN": "06",
    "JUL": "07",
    "AUG": "08",
    "SEP": "09",
    "OCT": "10",
    "NOV": "11",
    "DEC": "12",
}


def normalize_ticker(value):
    """
    Standardize company identifiers.

    Examples:
    ---------
    'abb'      -> 'ABB'
    ' Abb '    -> 'ABB'
    'HdfcBank' -> 'HDFCBANK'
    None       -> None
    """

    if pd.isna(value):
        return None

    return str(value).strip().upper()


def normalize_year(value):
    """
    Standardize year formats.

    Supported inputs:
    -----------------
    Dec 2012 -> 2012-12
    Mar 2014 -> 2014-03
    Mar-13   -> 2013-03
    Mar-14   -> 2014-03
    2024     -> 2024

    Returns:
    --------
    str | None
    """

    if pd.isna(value):
        return None

    value = str(value).strip()

    if re.fullmatch(r"\d{4}", value):
        return value

    match = re.fullmatch(r"([A-Za-z]{3})\s+(\d{4})", value)

    if match:
        month, year = match.groups()

        month = month.upper()

        if month in MONTH_MAP:
            return f"{year}-{MONTH_MAP[month]}"

    match = re.fullmatch(r"([A-Za-z]{3})-(\d{2})", value)

    if match:
        month, year = match.groups()

        month = month.upper()

        if month in MONTH_MAP:
            year = f"20{year}"
            return f"{year}-{MONTH_MAP[month]}"

    # Unsupported format
    return None
