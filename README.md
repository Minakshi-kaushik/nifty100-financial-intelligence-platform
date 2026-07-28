#  NIFTY100 Financial Analytics Platform

A comprehensive Financial Analytics Platform built to analyze NIFTY100 companies using financial statements, advanced analytics, stock screening, peer benchmarking, portfolio insights, and REST APIs.

The platform performs end-to-end ETL, computes over 50 financial metrics, generates analytical reports, and exposes data through FastAPI endpoints for further integration.

---

##  Features

###  ETL & Data Management
- Automated data loading into SQLite
- Schema validation and integrity checks
- Duplicate removal and data quality validation
- Audit report generation
- Incremental database loading

---

###  Financial Ratio Engine

Computes key financial metrics from Profit & Loss, Balance Sheet, and Cash Flow statements.

#### Profitability Ratios
- Net Profit Margin
- Operating Profit Margin
- Return on Equity (ROE)
- Return on Capital Employed (ROCE)
- Return on Assets (ROA)

#### Leverage Ratios
- Debt to Equity
- Interest Coverage Ratio
- Net Debt

#### Efficiency Ratios
- Asset Turnover
- Book Value per Share
- Earnings Per Share

#### Cash Flow KPIs
- Free Cash Flow
- Cash From Operations
- Capex
- FCF Conversion
- CFO Quality Score
- Capital Allocation Pattern

---

##  CAGR Analytics

Historical growth analysis including:

- Revenue CAGR (3Y, 5Y, 10Y)
- PAT CAGR (3Y, 5Y, 10Y)
- EPS CAGR (3Y, 5Y, 10Y)

Edge cases handled:

- Turnaround companies
- Loss-making businesses
- Zero base values
- Negative earnings
- Insufficient historical data

---

##  Composite Quality Score

Each company receives a quality score based on:

- ROE
- Debt Levels
- Cash Flow Quality
- Revenue Growth

This score powers stock screening and company ranking.

---

##  Stock Screener

Supports configurable screening strategies using YAML-based presets.

Available presets include:

- Quality Compounder
- Growth Accelerator
- Value Pick
- Dividend Champion
- Debt-Free Bluechip
- Turnaround Watch

Filters include:

- ROE
- Debt to Equity
- Revenue CAGR
- PAT CAGR
- EPS CAGR
- Free Cash Flow
- Dividend Payout
- Interest Coverage
- Asset Turnover

---

##  Peer Analytics

Performs sector-wise benchmarking by computing percentile rankings across peer groups.

Metrics compared include:

- ROE
- ROCE
- Net Profit Margin
- Revenue CAGR
- PAT CAGR
- EPS CAGR
- Debt to Equity
- Interest Coverage
- Asset Turnover
- Free Cash Flow

---

##  Reports

Automatically generates analytical reports including:

- Company Tearsheet
- Portfolio Summary
- Sector Report
- Peer Comparison Report

---

##  Portfolio Analytics

Portfolio level insights including:

- Portfolio composition
- Quality score aggregation
- Financial performance summary
- Risk analysis
- Sector allocation

---

##  REST APIs

Built using **FastAPI**.

Available endpoints include:

- Companies
- Portfolio
- Screener
- Peer Analytics
- Documents
- Health Check

---

##  Database

SQLite is used as the analytical data warehouse.

Major tables include:

- companies
- sectors
- market_cap
- stock_prices
- balancesheet
- profitandloss
- cashflow
- financial_ratios
- peer_groups
- peer_percentiles
- documents
- analysis
- prosandcons

---

##  Project Structure

```text
src/
│
├── analytics/
│   ├── ratio_engine.py
│   ├── ratios.py
│   ├── cashflow_kpis.py
│   ├── cashflow_kpis_initial.py
│   ├── cagr.py
│   ├── valuation.py
│   ├── peer.py
│   ├── peer_report.py
│   ├── radar.py
│   ├── clustering.py
│   └── capital_allocation_export.py
│
├── api/
│   └── routers/
│       ├── companies.py
│       ├── screener.py
│       ├── peers.py
│       ├── portfolio.py
│       ├── documents.py
│       └── health.py
│
├── reports/
│   ├── tearsheet.py
│   ├── portfolio_summary.py
│   └── sector_report.py
│
├── screener/
│
├── nlp/
│
└── db/
```

---

## 🛠 Tech Stack

### Programming

- Python

### Data Processing

- Pandas
- NumPy

### Database

- SQLite

### APIs

- FastAPI
- Uvicorn

### Configuration

- YAML

### Testing

- PyTest
- unittest

---

##  Outputs

The platform generates:

- Financial Ratio Database
- Capital Allocation Report
- Load Audit Report
- Peer Percentile Table
- Portfolio Reports
- Sector Reports
- Company Tear Sheets

---

##  Workflow

```text
Financial Statements
        │
        ▼
ETL & Validation
        │
        ▼
SQLite Database
        │
        ▼
Ratio Engine
        │
        ▼
CAGR Analytics
        │
        ▼
Cash Flow KPIs
        │
        ▼
Composite Quality Score
        │
        ▼
Stock Screener
        │
        ▼
Peer Analytics
        │
        ▼
Reports & APIs
```

---

##  Key Highlights

- End-to-End Financial Analytics Pipeline
- Automated ETL Workflow
- 50+ Financial Metrics
- Growth Analytics using CAGR
- Portfolio Analytics
- Peer Benchmarking
- Stock Screening Engine
- Report Generation
- REST APIs
- Modular & Scalable Architecture

---

## Future Enhancements

- Interactive Dashboard
- Live NSE/BSE Market Data Integration
- Portfolio Optimizer
- AI-based Stock Recommendation Engine
- Time-Series Forecasting
- Automated Report Scheduling

---

## Author

**Minakshi Kaushik**

B.Tech Computer Science Engineering  
Indira Gandhi Delhi Technical University for Women (IGDTUW)

---

## License

This project is intended for educational, analytical, and research purposes.