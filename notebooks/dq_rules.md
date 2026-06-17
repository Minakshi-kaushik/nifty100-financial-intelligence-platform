# Sprint 1 - Data Quality Rules Specification

## Project

Nifty100 Financial Intelligence Platform

## Sprint

Sprint 1 – Day 03

## Objective

The objective of Data Quality Validation is to ensure all source datasets satisfy integrity, consistency, completeness, and business validation rules before loading data into the SQLite database.

Validation results will be written to:

```text
output/validation_failures.csv
```

Each validation failure must include:

* rule_id
* severity
* table_name
* company_id
* year
* issue_description

---

# Severity Levels

## CRITICAL

Data load must be stopped until the issue is resolved.

Examples:

* Duplicate primary keys
* Foreign key violations
* Missing company identifiers
* Invalid financial records

---

## WARNING

Data may be loaded but should be reviewed manually.

Examples:

* Unusual profitability
* Suspicious ratios
* Missing historical coverage

---

# Actual Dataset Column Mapping

## companies.xlsx

| Business Field | Dataset Column  |
| -------------- | --------------- |
| Primary Key    | id              |
| Company Name   | company_name    |
| Website        | website         |
| NSE Profile    | nse_profile     |
| BSE Profile    | bse_profile     |
| ROCE           | roce_percentage |
| ROE            | roe_percentage  |

---

## profitandloss.xlsx

| Business Field     | Dataset Column   |
| ------------------ | ---------------- |
| Primary Key        | id               |
| Company Identifier | company_id       |
| Year               | year             |
| Sales              | sales            |
| Expenses           | expenses         |
| Operating Profit   | operating_profit |
| OPM                | opm_percentage   |
| Tax Rate           | tax_percentage   |
| Net Profit         | net_profit       |
| EPS                | eps              |
| Dividend Payout    | dividend_payout  |

---

## balancesheet.xlsx

| Business Field     | Dataset Column    |
| ------------------ | ----------------- |
| Primary Key        | id                |
| Company Identifier | company_id        |
| Year               | year              |
| Total Liabilities  | total_liabilities |
| Total Assets       | total_assets      |
| Equity Capital     | equity_capital    |
| Reserves           | reserves          |
| Borrowings         | borrowings        |

---

## cashflow.xlsx

| Business Field     | Dataset Column     |
| ------------------ | ------------------ |
| Primary Key        | id                 |
| Company Identifier | company_id         |
| Year               | year               |
| Operating Activity | operating_activity |
| Investing Activity | investing_activity |
| Financing Activity | financing_activity |
| Net Cash Flow      | net_cash_flow      |

---

## documents.xlsx

| Business Field     | Dataset Column |
| ------------------ | -------------- |
| Primary Key        | id             |
| Company Identifier | company_id     |
| Year               | Year           |
| Annual Report      | Annual_Report  |

---

# Data Quality Rules

## DQ-01 Primary Key Uniqueness

### Severity

CRITICAL

### Description

Primary key values must be unique within a table.

### Validation

No duplicate values allowed in:

* companies.id
* profitandloss.id
* balancesheet.id
* cashflow.id
* documents.id

---

## DQ-02 Company-Year Uniqueness

### Severity

CRITICAL

### Description

Each company-year combination should appear only once.

### Validation

Unique:

(company_id, year)

for:

* profitandloss
* balancesheet
* cashflow

---

## DQ-03 Foreign Key Integrity

### Severity

CRITICAL

### Description

Every company_id must exist in the master companies dataset.

### Validation

Child tables:

* profitandloss
* balancesheet
* cashflow
* documents

must reference a valid company.

---

## DQ-04 Balance Sheet Equation Validation

### Severity

CRITICAL

### Description

Balance Sheet should approximately balance.

### Validation

total_assets ≈ total_liabilities

Tolerance:

1%

---

## DQ-05 Operating Margin Cross-Check

### Severity

WARNING

### Description

Reported operating margin should match calculated operating margin.

### Validation

Calculated OPM:

((sales - expenses) / sales) × 100

Compare with:

opm_percentage

Tolerance:

±1%

---

## DQ-06 Positive Sales Validation

### Severity

CRITICAL

### Description

Revenue must be positive.

### Validation

sales > 0

---

## DQ-07 Positive Assets Validation

### Severity

CRITICAL

### Description

Total assets should be positive.

### Validation

total_assets > 0

---

## DQ-08 Positive Liabilities Validation

### Severity

CRITICAL

### Description

Total liabilities should be positive.

### Validation

total_liabilities > 0

---

## DQ-09 Net Cash Flow Reconciliation

### Severity

WARNING

### Description

Net cash flow should reconcile with component activities.

### Validation

operating_activity +
investing_activity +
financing_activity

≈ net_cash_flow

Tolerance:

±1%

---

## DQ-10 Tax Rate Validation

### Severity

WARNING

### Description

Tax percentage should remain within a realistic range.

### Validation

0 ≤ tax_percentage ≤ 60

---

## DQ-11 Dividend Payout Validation

### Severity

WARNING

### Description

Dividend payout ratio should remain within reasonable limits.

### Validation

0 ≤ dividend_payout ≤ 150

---

## DQ-12 URL Validation

### Severity

WARNING

### Description

Company URLs and annual report links should be valid.

### Validation

Must begin with:

* http://
* https://

Fields:

* website
* nse_profile
* bse_profile
* Annual_Report

---

## DQ-13 EPS Sign Consistency

### Severity

WARNING

### Description

EPS sign should align with net profit sign.

### Validation

If:

net_profit > 0

then:

eps > 0

If:

net_profit < 0

then:

eps < 0

---

## DQ-14 Historical Coverage Validation

### Severity

WARNING

### Description

Companies should have sufficient historical financial coverage.

### Validation

Minimum:

5 years of available records

Tables:

* profitandloss
* balancesheet
* cashflow

---

## DQ-15 Critical Null Validation

### Severity

CRITICAL

### Description

Business key fields must never be null.

### Validation

No null values allowed in:

* company_id
* year

---

## DQ-16 Duplicate Company Name Validation

### Severity

WARNING

### Description

Company names should be unique within the master dataset.

### Validation

No duplicate:

company_name

---

# Validation Output Specification

## File

output/validation_failures.csv

## Columns

| Column            | Description                |
| ----------------- | -------------------------- |
| rule_id           | DQ Rule Identifier         |
| severity          | CRITICAL / WARNING         |
| table_name        | Dataset Name               |
| company_id        | Company Identifier         |
| year              | Financial Year             |
| issue_description | Validation Failure Details |

---

# Exit Criteria

The validator is considered complete when:

* All 16 DQ rules are implemented
* validation_failures.csv is generated successfully
* All CRITICAL issues are resolved
* Foreign key integrity passes
* Primary key uniqueness passes
* Company-year uniqueness passes
* Validation report reviewed before database load

---

# Sprint Deliverable

Files:

* src/etl/validator.py
* output/validation_failures.csv
* notebooks/dq_rules.md


