# Manual Data Quality Review

## Objective

Perform manual inspection of randomly selected companies to verify data consistency across tables.

---

## Company 1: ABB

Reviewed Tables:

* companies
* profitandloss
* balancesheet
* cashflow
* financial_ratios

Findings:

* Company exists in master table.
* Financial years available from Dec 2012 to Mar 2024.
* Cashflow records present.
* Balance sheet records present.
* No missing company identifiers.

Status: PASS

---

## Company 2: HDFCBANK

Reviewed Tables:

* companies
* profitandloss
* balancesheet
* cashflow

Findings:

* Records available across major datasets.
* Company identifier consistent.
* Year values properly populated.

Status: PASS

---

## Company 3: RELIANCE

Reviewed Tables:

* companies
* profitandloss
* balancesheet
* cashflow

Findings:

* Cross-table consistency verified.
* No orphan records found.

Status: PASS

---

## Company 4: TCS

Reviewed Tables:

* companies
* profitandloss
* balancesheet
* cashflow

Findings:

* Financial data present.
* Year coverage acceptable.

Status: PASS

---

## Company 5: INFY

Reviewed Tables:

* companies
* profitandloss
* balancesheet
* cashflow

Findings:

* Data loaded successfully.
* Company identifiers consistent.

Status: PASS

---

## Summary

Companies Reviewed: 5

Passed: 5

Failed: 0

Critical Issues: 0

Conclusion:
Manual review completed successfully. Dataset is suitable for analytics and reporting.
