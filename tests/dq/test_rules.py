import pandas as pd

from src.etl.validator import DataValidator


# ==========================================================
# DQ-01 Primary Key Uniqueness
# ==========================================================


def test_primary_key_duplicates():

    validator = DataValidator()

    df = pd.DataFrame(
        {
            "id": [1, 1],
            "company_id": ["ABC", "ABC"],
            "year": ["2024", "2024"],
        }
    )

    validator.check_primary_key_uniqueness(df, "companies")

    assert len(validator.failures) == 2
    assert validator.failures[0].rule_id == "DQ-01"


def test_primary_key_pass():

    validator = DataValidator()

    df = pd.DataFrame(
        {
            "id": [1, 2],
            "company_id": ["ABC", "XYZ"],
            "year": ["2024", "2024"],
        }
    )

    validator.check_primary_key_uniqueness(df, "companies")

    assert len(validator.failures) == 0


# ==========================================================
# DQ-02 Company-Year Uniqueness
# ==========================================================


def test_company_year_duplicates():

    validator = DataValidator()

    df = pd.DataFrame(
        {
            "company_id": ["ABC", "ABC"],
            "year": ["2024", "2024"],
        }
    )

    validator.check_company_year_uniqueness(df, "profitandloss")

    assert len(validator.failures) == 2
    assert validator.failures[0].rule_id == "DQ-02"


def test_company_year_pass():

    validator = DataValidator()

    df = pd.DataFrame(
        {
            "company_id": ["ABC", "XYZ"],
            "year": ["2024", "2024"],
        }
    )

    validator.check_company_year_uniqueness(df, "profitandloss")

    assert len(validator.failures) == 0


# ==========================================================
# DQ-03 Foreign Key Integrity
# ==========================================================


def test_foreign_key_failure():

    validator = DataValidator()

    parent = pd.DataFrame(
        {
            "id": ["ABC", "XYZ"],
        }
    )

    child = pd.DataFrame(
        {
            "company_id": ["ABC", "INVALID"],
            "year": ["2024", "2024"],
        }
    )

    validator.check_foreign_key_integrity(
        child,
        parent,
        "balancesheet",
    )

    assert len(validator.failures) == 1
    assert validator.failures[0].rule_id == "DQ-03"


def test_foreign_key_pass():

    validator = DataValidator()

    parent = pd.DataFrame(
        {
            "id": ["ABC", "XYZ"],
        }
    )

    child = pd.DataFrame(
        {
            "company_id": ["ABC", "XYZ"],
            "year": ["2024", "2024"],
        }
    )

    validator.check_foreign_key_integrity(
        child,
        parent,
        "balancesheet",
    )

    assert len(validator.failures) == 0


# ==========================================================
# ValidationFailure object
# ==========================================================


def test_validation_failure_to_dict():

    validator = DataValidator()

    validator.add_failure(
        "DQ-01",
        "CRITICAL",
        "companies",
        "ABC",
        "2024",
        "Duplicate ID",
    )

    failure = validator.failures[0].to_dict()

    assert failure["rule_id"] == "DQ-01"
    assert failure["severity"] == "CRITICAL"
    assert failure["company_id"] == "ABC"


# ==========================================================
# Save Report
# ==========================================================


def test_save_report(tmp_path):

    validator = DataValidator()

    validator.add_failure(
        "DQ-01",
        "CRITICAL",
        "companies",
        "ABC",
        "2024",
        "Duplicate",
    )

    outfile = tmp_path / "validation.csv"

    validator.save_report(outfile)

    assert outfile.exists()
