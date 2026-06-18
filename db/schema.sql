PRAGMA foreign_keys = OFF;

-- =====================================================
-- COMPANIES
-- =====================================================

CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY,
    company_id TEXT UNIQUE,
    company_name TEXT,
    chart_link TEXT,
    about_company TEXT
);

-- =====================================================
-- SECTORS
-- =====================================================

CREATE TABLE IF NOT EXISTS sectors (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    broad_sector TEXT,
    sub_sector TEXT,
    index_weight REAL,
    market_cap_category TEXT
);

-- =====================================================
-- ANALYSIS
-- =====================================================

CREATE TABLE IF NOT EXISTS analysis (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    compounded_sales_growth TEXT,
    compounded_profit_growth TEXT,
    stock_price_cagr TEXT,
    roe TEXT
);

-- =====================================================
-- BALANCE SHEET
-- =====================================================

CREATE TABLE IF NOT EXISTS balancesheet (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    year TEXT,

    equity_capital REAL,
    reserves REAL,
    borrowing REAL,
    other_liabilities REAL,
    total_liabilities REAL,

    fixed_assets REAL,
    cwip REAL,
    investment REAL,
    other_assets REAL,
    total_assets REAL
);

-- =====================================================
-- CASH FLOW
-- =====================================================

CREATE TABLE IF NOT EXISTS cashflow (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    year TEXT,

    operating_activity REAL,
    investing_activity REAL,
    financing_activity REAL,
    net_cash_flow REAL
);

-- =====================================================
-- DOCUMENTS
-- =====================================================

CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    year INTEGER,
    annual_report TEXT
);

-- =====================================================
-- FINANCIAL RATIOS
-- =====================================================

CREATE TABLE IF NOT EXISTS financial_ratios (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    year TEXT,

    net_profit REAL,
    operating_margin REAL,
    return_on_equity REAL,
    debt_to_equity REAL,
    interest_coverage REAL,
    asset_turnover REAL,

    free_cash_flow REAL,
    capex REAL,

    earnings_per_share REAL,
    book_value REAL,
    dividend_yield REAL,

    total_debt REAL,
    cash_from_operations REAL
);

-- =====================================================
-- MARKET CAP
-- =====================================================

CREATE TABLE IF NOT EXISTS market_cap (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    year INTEGER,

    market_cap REAL,
    enterprise_value REAL,

    pe_ratio REAL,
    pb_ratio REAL,
    ev_ebitda REAL,
    dividend_yield_pct REAL
);

-- =====================================================
-- PEER GROUPS
-- =====================================================

CREATE TABLE IF NOT EXISTS peer_groups (
    id INTEGER PRIMARY KEY,
    peer_group TEXT,
    company_id TEXT,
    is_benchmark BOOLEAN
);

-- =====================================================
-- PROFIT & LOSS
-- =====================================================

CREATE TABLE IF NOT EXISTS profitandloss (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    year TEXT,

    sales REAL,
    expenses REAL,
    operating_profit REAL,
    opm_percentage REAL,

    other_income REAL,
    interest REAL,
    depreciation REAL,

    profit_before_tax REAL,
    tax_percentage REAL,
    net_profit REAL
);

-- =====================================================
-- PROS AND CONS
-- =====================================================

CREATE TABLE IF NOT EXISTS prosandcons (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    pros TEXT,
    cons TEXT
);

-- =====================================================
-- STOCK PRICES
-- =====================================================

CREATE TABLE IF NOT EXISTS stock_prices (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    trade_date TEXT,

    open_price REAL,
    high_price REAL,
    low_price REAL,
    close_price REAL,

    volume REAL,
    adjusted_close REAL
);

-- =====================================================
-- INDEXES
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_companies_company_id
ON companies(company_id);

CREATE INDEX IF NOT EXISTS idx_analysis_company
ON analysis(company_id);

CREATE INDEX IF NOT EXISTS idx_balancesheet_company
ON balancesheet(company_id);

CREATE INDEX IF NOT EXISTS idx_cashflow_company
ON cashflow(company_id);

CREATE INDEX IF NOT EXISTS idx_documents_company
ON documents(company_id);

CREATE INDEX IF NOT EXISTS idx_financial_ratios_company
ON financial_ratios(company_id);

CREATE INDEX IF NOT EXISTS idx_market_cap_company
ON market_cap(company_id);

CREATE INDEX IF NOT EXISTS idx_peer_groups_company
ON peer_groups(company_id);

CREATE INDEX IF NOT EXISTS idx_profitandloss_company
ON profitandloss(company_id);

CREATE INDEX IF NOT EXISTS idx_prosandcons_company
ON prosandcons(company_id);

CREATE INDEX IF NOT EXISTS idx_stock_prices_company
ON stock_prices(company_id);