# Sprint 1 - Dataset Profiling Report

## Project

Nifty100 Financial Intelligence Platform

## Sprint

Sprint 1 - Data Foundation

## Purpose

This document records the initial profiling of all source datasets before ETL development. The objective is to identify:

* Dataset structure
* Sheet names
* Header row positions
* Record counts
* Column counts
* Identifier columns
* Year columns
* Data quality concerns
* Loader requirements

---

# Dataset Summary

| File                  | Rows | Columns | Header Row | Notes                           |
| --------------------- | ---- | ------- | ---------- | ------------------------------- |
| analysis.xlsx         | 1189 | 12      | TBD        | Needs header validation         |
| balancesheet.xlsx     | 1313 | 13      | TBD        | Needs header validation         |
| cashflow.xlsx         | 1188 | 9       | TBD        | Needs header validation         |
| companies.xlsx        | 93   | 12      | TBD        | Contains company master data    |
| documents.xlsx        | 93   | 6       | TBD        | Contains annual report metadata |
| financial_ratios.xlsx | 1190 | 18      | 0          | Appears correctly structured    |
| market_cap.xlsx       | 92   | 3       | 0          | Appears correctly structured    |
| peer_groups.xlsx      | 92   | 3       | 0          | Appears correctly structured    |
| profitandloss.xlsx    | 1277 | 14      | TBD        | Needs header validation         |
| prosandcons.xlsx      | 92   | 4       | TBD        | Needs header validation         |
| sectors.xlsx          | 92   | 3       | 0          | Appears correctly structured    |
| stock_prices.xlsx     | 5520 | 4       | 0          | Appears correctly structured    |

---

# Detailed Dataset Inspection

## companies.xlsx

### Initial Observations

* Row Count: 93
* Column Count: 12
* Sheet Count: 1

### Header Investigation

Observed first row appears to contain metadata rather than actual column names.

Likely requires:

```python
pd.read_excel(file, header=1)
```

### Expected Purpose

Master company dimension table.

### Candidate Identifier Columns

To be confirmed after header validation.

### Notes

Used as parent table for foreign key relationships.

---

## profitandloss.xlsx

### Initial Observations

* Row Count: 1277
* Column Count: 14

### Header Investigation

Likely requires header=1.

### Expected Contents

* Sales
* Operating Profit
* EBITDA
* PAT
* EPS

### Notes

Primary source for profitability metrics.

---

## balancesheet.xlsx

### Initial Observations

* Row Count: 1313
* Column Count: 13

### Expected Contents

* Assets
* Liabilities
* Equity
* Debt

### Notes

Will be used for DQ-04 Balance Sheet Validation.

---

## cashflow.xlsx

### Initial Observations

* Row Count: 1188
* Column Count: 9

### Expected Contents

* CFO
* CFI
* CFF

### Notes

Used for Free Cash Flow calculations.

---

## analysis.xlsx

### Initial Observations

* Row Count: 1189
* Column Count: 12

### Notes

Likely contains calculated company metrics.

---

## documents.xlsx

### Initial Observations

* Row Count: 93
* Column Count: 6

### Notes

Expected to contain annual report URLs and metadata.

---

## prosandcons.xlsx

### Initial Observations

* Row Count: 92
* Column Count: 4

### Notes

Expected to contain qualitative company commentary.

---

## sectors.xlsx

### Initial Observations

* Row Count: 92
* Column Count: 3

### Status

Appears correctly structured.

---

## peer_groups.xlsx

### Initial Observations

* Row Count: 92
* Column Count: 3

### Status

Appears correctly structured.

---

## market_cap.xlsx

### Initial Observations

* Row Count: 92
* Column Count: 3

### Status

Appears correctly structured.

---

## stock_prices.xlsx

### Initial Observations

* Row Count: 5520
* Column Count: 4

### Status

Appears correctly structured.

### Notes

Expected source for historical market data.

---

## financial_ratios.xlsx

### Initial Observations

* Row Count: 1190
* Column Count: 18

### Status

Appears correctly structured.

### Notes

Will be useful for validation of calculated ratios in later sprints.

---

# Preliminary Findings

1. Multiple datasets appear to contain metadata rows above actual headers.
2. Header row validation is required before implementing loader.py.
3. Companies dataset is likely the parent/master table.
4. Foreign key relationships will need to be confirmed during schema design.
5. Year format normalization requirements remain to be identified.
6. Company identifier normalization requirements remain to be identified.

---

---

# Header Validation Summary

| File | Header Row | Status |
|--------|--------|--------|
| analysis.xlsx | 1 | Metadata row detected |
| balancesheet.xlsx | 1 | Metadata row detected |
| cashflow.xlsx | 1 | Metadata row detected |
| companies.xlsx | 1 | Metadata row detected |
| documents.xlsx | 1 | Metadata row detected |
| profitandloss.xlsx | 1 | Metadata row detected |
| prosandcons.xlsx | 1 | Metadata row detected |
| financial_ratios.xlsx | 0 | Clean structure |
| market_cap.xlsx | 0 | Clean structure |
| peer_groups.xlsx | 0 | Clean structure |
| sectors.xlsx | 0 | Clean structure |
| stock_prices.xlsx | 0 | Clean structure |

---

# Company Identifier Discovery

The primary identifier used across datasets is:

company_id

Example values:

- ABB
- TCS
- HDFCBANK
- ADANIENT
- RELIANCE

This field will be standardized using:

normalize_ticker()

during ETL processing.

---

# Year Column Discovery

## balancesheet.xlsx

Column:
year

Example values:

- Dec 2012
- Mar 2014
- Mar 2015

---

## cashflow.xlsx

Column:
year

Example values:

- Dec 2012
- Mar 2014
- Mar 2015

---

## profitandloss.xlsx

Column:
year

Example values:

- Mar-13
- Mar-14
- Mar-15

---

## financial_ratios.xlsx

Column:
year

Example values:

- 2019
- 2020
- 2021
- 2022
- 2023

---

## market_cap.xlsx

Column:
year

Example values:

- 2024

---

## documents.xlsx

Column:
Year

Example values:

- 2024
- 2023
- 2022

---

# Loader Requirements

## Files Requiring

```python
pd.read_excel(file, header=1)