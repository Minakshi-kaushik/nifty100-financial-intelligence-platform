# Sprint 2 Retrospective

## Objective

Build a complete Financial Ratio Engine capable of computing profitability,
leverage, efficiency, growth and cash-flow KPIs for every company-year.

---

## Major Deliverables

- ratios.py
- cagr.py
- cashflow_kpis.py
- ratio_engine.py
- financial_ratios SQLite table
- capital_allocation.csv
- ratio_edge_cases.log

---

## Formula Decisions

- ROE returns None when equity <= 0
- Debt Free companies return D/E = 0
- Interest Coverage returns None when interest = 0
- Debt Free label stored separately
- Financial companies exempt from High Leverage warning
- CAGR engine handles turnaround and decline cases using flags
- FCF calculated as CFO + Investing Activity

---

## Edge Cases Handled

- Negative Equity
- Zero Sales
- Zero Assets
- Zero Interest
- Zero PAT
- Missing Cashflow
- Bank Leverage
- CAGR Turnarounds
- Duplicate Excel rows

---

## Database Issues Resolved

- Duplicate company-year records removed
- Loader rebuilt to recreate database
- Duplicate validation scripts added
- Ratio Engine updated to avoid duplicate inserts

---

## Validation

- KPI unit tests passed
- Database validation passed
- Duplicate validation passed
- Manual spot check completed
- Capital Allocation export verified

---

## Sprint Outcome

Sprint 2 successfully produced a complete financial ratio engine capable of
generating profitability, leverage, efficiency, CAGR and cash-flow KPIs for
all company-years in the dataset.