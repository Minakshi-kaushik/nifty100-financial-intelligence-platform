import sys
from pathlib import Path
import pandas as pd

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.etl.validator import DataValidator


def load_excel(file_name, header):
    return pd.read_excel(PROJECT_ROOT / "data" / "raw" / file_name, header=header)


def main():

    print("Loading datasets...")

    companies = load_excel("companies.xlsx", header=1)

    profitandloss = load_excel("profitandloss.xlsx", header=1)

    balancesheet = load_excel("balancesheet.xlsx", header=1)

    cashflow = load_excel("cashflow.xlsx", header=1)

    documents = load_excel("documents.xlsx", header=1)

    validator = DataValidator()

    print("Running DQ-01...")

    validator.check_primary_key_uniqueness(companies, "companies")

    validator.check_primary_key_uniqueness(profitandloss, "profitandloss")

    validator.check_primary_key_uniqueness(balancesheet, "balancesheet")

    validator.check_primary_key_uniqueness(cashflow, "cashflow")

    validator.check_primary_key_uniqueness(documents, "documents")

    print("Running DQ-02...")

    validator.check_company_year_uniqueness(profitandloss, "profitandloss")

    validator.check_company_year_uniqueness(balancesheet, "balancesheet")

    validator.check_company_year_uniqueness(cashflow, "cashflow")

    print("Running DQ-03...")

    validator.check_foreign_key_integrity(profitandloss, companies, "profitandloss")

    validator.check_foreign_key_integrity(balancesheet, companies, "balancesheet")

    validator.check_foreign_key_integrity(cashflow, companies, "cashflow")

    validator.check_foreign_key_integrity(documents, companies, "documents")

    validator.save_report()

    print("\nValidation Complete")
    print(f"Failures Found: {len(validator.failures)}")


if __name__ == "__main__":
    main()
