import sqlite3
from pathlib import Path

import pandas as pd
import pytest

from db.loader import (
    create_database,
    load_table,
)


# =====================================================
# DATABASE CREATION
# =====================================================


def test_database_created():

    conn = create_database()

    assert isinstance(conn, sqlite3.Connection)

    conn.close()


# =====================================================
# LOAD TABLE
# =====================================================


def test_load_table_returns_dict(tmp_path):

    conn = sqlite3.connect(":memory:")

    conn.execute("""
        CREATE TABLE companies(
            company_id TEXT,
            year TEXT
        )
    """)

    file = tmp_path / "companies.xlsx"

    df = pd.DataFrame({"company_id": ["ABC"], "year": ["2024"]})

    df.to_excel(file, index=False)

    result = load_table(
        conn,
        "companies",
        file,
        0,
    )

    assert isinstance(result, dict)

    conn.close()


def test_rows_loaded(tmp_path):

    conn = sqlite3.connect(":memory:")

    conn.execute("""
        CREATE TABLE companies(
            company_id TEXT,
            year TEXT
        )
    """)

    file = tmp_path / "companies.xlsx"

    df = pd.DataFrame({"company_id": ["ABC", "XYZ"], "year": ["2024", "2024"]})

    df.to_excel(file, index=False)

    result = load_table(conn, "companies", file, 0)

    assert result["rows_loaded"] == 2

    conn.close()


def test_rows_rejected_zero(tmp_path):

    conn = sqlite3.connect(":memory:")

    conn.execute("""
        CREATE TABLE companies(
            company_id TEXT,
            year TEXT
        )
    """)

    file = tmp_path / "companies.xlsx"

    pd.DataFrame({"company_id": ["ABC"], "year": ["2024"]}).to_excel(file, index=False)

    result = load_table(conn, "companies", file, 0)

    assert result["rows_rejected"] == 0

    conn.close()


def test_duplicate_removed(tmp_path):

    conn = sqlite3.connect(":memory:")

    conn.execute("""
        CREATE TABLE companies(
            company_id TEXT,
            year TEXT
        )
    """)

    file = tmp_path / "companies.xlsx"

    pd.DataFrame({"company_id": ["ABC", "ABC"], "year": ["2024", "2024"]}).to_excel(
        file, index=False
    )

    result = load_table(conn, "companies", file, 0)

    assert result["rows_loaded"] == 1

    conn.close()


def test_column_lowercase(tmp_path):

    conn = sqlite3.connect(":memory:")

    conn.execute("""
        CREATE TABLE companies(
            company_id TEXT,
            year TEXT
        )
    """)

    file = tmp_path / "companies.xlsx"

    pd.DataFrame({"Company ID": ["ABC"], "Year": ["2024"]}).to_excel(file, index=False)

    load_table(conn, "companies", file, 0)

    cur = conn.cursor()

    cur.execute("SELECT company_id FROM companies")

    row = cur.fetchone()

    assert row[0] == "ABC"

    conn.close()


def test_spaces_removed(tmp_path):

    conn = sqlite3.connect(":memory:")

    conn.execute("""
        CREATE TABLE companies(
            company_id TEXT,
            year TEXT
        )
    """)

    file = tmp_path / "companies.xlsx"

    pd.DataFrame({"company id": ["ABC"], "year": ["2024"]}).to_excel(file, index=False)

    load_table(conn, "companies", file, 0)

    count = conn.execute("SELECT COUNT(*) FROM companies").fetchone()[0]

    assert count == 1

    conn.close()


def test_hyphen_removed(tmp_path):

    conn = sqlite3.connect(":memory:")

    conn.execute("""
        CREATE TABLE companies(
            company_id TEXT,
            year TEXT
        )
    """)

    file = tmp_path / "companies.xlsx"

    pd.DataFrame({"company-id": ["ABC"], "year": ["2024"]}).to_excel(file, index=False)

    load_table(conn, "companies", file, 0)

    count = conn.execute("SELECT COUNT(*) FROM companies").fetchone()[0]

    assert count == 1

    conn.close()


def test_dictionary_keys(tmp_path):

    conn = sqlite3.connect(":memory:")

    conn.execute("""
        CREATE TABLE companies(
            company_id TEXT,
            year TEXT
        )
    """)

    file = tmp_path / "companies.xlsx"

    pd.DataFrame({"company_id": ["ABC"], "year": ["2024"]}).to_excel(file, index=False)

    result = load_table(conn, "companies", file, 0)

    assert "table_name" in result
    assert "rows_loaded" in result
    assert "rows_rejected" in result

    conn.close()


def test_table_name(tmp_path):

    conn = sqlite3.connect(":memory:")

    conn.execute("""
        CREATE TABLE companies(
            company_id TEXT,
            year TEXT
        )
    """)

    file = tmp_path / "companies.xlsx"

    pd.DataFrame({"company_id": ["ABC"], "year": ["2024"]}).to_excel(file, index=False)

    result = load_table(conn, "companies", file, 0)

    assert result["table_name"] == "companies"

    conn.close()
