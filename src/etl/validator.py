from pathlib import Path
import pandas as pd


class ValidationFailure:
    def __init__(
        self,
        rule_id,
        severity,
        table_name,
        company_id,
        year,
        issue_description,
    ):
        self.rule_id = rule_id
        self.severity = severity
        self.table_name = table_name
        self.company_id = company_id
        self.year = year
        self.issue_description = issue_description

    def to_dict(self):
        return {
            "rule_id": self.rule_id,
            "severity": self.severity,
            "table_name": self.table_name,
            "company_id": self.company_id,
            "year": self.year,
            "issue_description": self.issue_description,
        }


class DataValidator:
    def __init__(self):
        self.failures = []

    def add_failure(
        self,
        rule_id,
        severity,
        table_name,
        company_id,
        year,
        issue_description,
    ):
        self.failures.append(
            ValidationFailure(
                rule_id,
                severity,
                table_name,
                company_id,
                year,
                issue_description,
            )
        )

    # ==================================================
    # DQ-01 Primary Key Uniqueness
    # ==================================================

    def check_primary_key_uniqueness(
        self,
        df,
        table_name,
        pk_column="id",
    ):

        duplicates = df[df.duplicated(subset=[pk_column], keep=False)]

        for _, row in duplicates.iterrows():
            self.add_failure(
                rule_id="DQ-01",
                severity="CRITICAL",
                table_name=table_name,
                company_id=row.get("company_id"),
                year=row.get("year"),
                issue_description=f"Duplicate primary key: {row[pk_column]}",
            )

    # ==================================================
    # DQ-02 Company-Year Uniqueness
    # ==================================================

    def check_company_year_uniqueness(
        self,
        df,
        table_name,
    ):

        duplicates = df[
            df.duplicated(
                subset=["company_id", "year"],
                keep=False,
            )
        ]

        for _, row in duplicates.iterrows():
            self.add_failure(
                rule_id="DQ-02",
                severity="CRITICAL",
                table_name=table_name,
                company_id=row["company_id"],
                year=row["year"],
                issue_description="Duplicate company-year combination",
            )

    # ==================================================
    # DQ-03 Foreign Key Integrity
    # ==================================================

    def check_foreign_key_integrity(
        self,
        child_df,
        parent_df,
        table_name,
    ):

        # Parent company master table uses id
        valid_companies = set(parent_df["id"])

        invalid_rows = child_df[~child_df["company_id"].isin(valid_companies)]

        for _, row in invalid_rows.iterrows():
            self.add_failure(
                rule_id="DQ-03",
                severity="CRITICAL",
                table_name=table_name,
                company_id=row["company_id"],
                year=row.get("year"),
                issue_description="Invalid foreign key",
            )

    # ==================================================
    # Save Validation Report
    # ==================================================

    def save_report(
        self,
        output_path="output/validation_failures.csv",
    ):

        Path("output").mkdir(exist_ok=True)

        report = pd.DataFrame([f.to_dict() for f in self.failures])

        report.to_csv(
            output_path,
            index=False,
        )

        print(f"Validation report saved: {output_path}")
