PRAGMA foreign_keys = OFF;

-- =====================================================
-- COMPANIES
-- =====================================================

CREATE TABLE companies (
    id TEXT PRIMARY KEY,
    company_logo TEXT,
    company_name TEXT,
    chart_link TEXT,
    about_company TEXT,
    website TEXT,
    nse_profile TEXT,
    bse_profile TEXT,
    face_value REAL,
    book_value REAL,
    roce_percentage REAL,
    roe_percentage REAL
);

-- =====================================================
-- ANALYSIS
-- =====================================================

CREATE TABLE analysis (
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

CREATE TABLE balancesheet (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    year TEXT,
    equity_capital REAL,
    reserves REAL,
    borrowings REAL,
    other_liabilities REAL,
    total_liabilities REAL,
    fixed_assets REAL,
    cwip REAL,
    investments REAL,
    other_asset REAL,
    total_assets REAL
);

-- =====================================================
-- CASHFLOW
-- =====================================================

CREATE TABLE cashflow (
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

CREATE TABLE documents (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    year INTEGER,
    annual_report TEXT
);

-- =====================================================
-- FINANCIAL RATIOS
-- =====================================================

CREATE TABLE financial_ratios (
    id INTEGER PRIMARY KEY,

    company_id TEXT NOT NULL,
    year TEXT NOT NULL,

    -- =====================================================
    -- Profitability Ratios
    -- =====================================================

    net_profit_margin_pct REAL,
    operating_profit_margin_pct REAL,
    return_on_equity_pct REAL,
    return_on_capital_employed_pct REAL,
    return_on_assets_pct REAL,

    -- =====================================================
    -- Leverage & Efficiency
    -- =====================================================

    debt_to_equity REAL,
    interest_coverage REAL,
    asset_turnover REAL,
    net_debt_cr REAL,

    high_leverage_flag INTEGER DEFAULT 0,
    icr_warning_flag INTEGER DEFAULT 0,
    icr_label TEXT,

    -- =====================================================
    -- Cash Flow KPIs
    -- =====================================================

    free_cash_flow_cr REAL,
    capex_cr REAL,
    fcf_conversion_pct REAL,
    cash_from_operations_cr REAL,
    cfo_quality_score REAL,
    cfo_quality_label TEXT,

    capital_allocation_pattern TEXT,

    -- =====================================================
    -- Per Share Metrics
    -- =====================================================

    earnings_per_share REAL,
    book_value_per_share REAL,
    dividend_payout_ratio_pct REAL,

    total_debt_cr REAL,

    -- =====================================================
    -- Growth Metrics
    -- =====================================================

    revenue_cagr_3yr REAL,
    revenue_cagr_5yr REAL,
    revenue_cagr_10yr REAL,

    pat_cagr_3yr REAL,
    pat_cagr_5yr REAL,
    pat_cagr_10yr REAL,

    eps_cagr_3yr REAL,
    eps_cagr_5yr REAL,
    eps_cagr_10yr REAL,

    revenue_cagr_flag TEXT,
    pat_cagr_flag TEXT,
    eps_cagr_flag TEXT,

    -- =====================================================
    -- Composite Score
    -- =====================================================

    composite_quality_score REAL,

    FOREIGN KEY(company_id)
        REFERENCES companies(id)
);

-- =====================================================
-- MARKET CAP
-- =====================================================

CREATE TABLE market_cap (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    year INTEGER,

    market_cap_crore REAL,
    enterprise_value_crore REAL,

    pe_ratio REAL,
    pb_ratio REAL,
    ev_ebitda REAL,
    dividend_yield_pct REAL
);

-- =====================================================
-- PEER GROUPS
-- =====================================================

CREATE TABLE peer_groups (
    id INTEGER PRIMARY KEY,
    peer_group_name TEXT,
    company_id TEXT,
    is_benchmark TEXT
);

-- =====================================================
-- PROFIT & LOSS
-- =====================================================

CREATE TABLE profitandloss (
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
    net_profit REAL,
    eps REAL,
    dividend_payout REAL
);

-- =====================================================
-- PROS & CONS
-- =====================================================

CREATE TABLE prosandcons (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    pros TEXT,
    cons TEXT
);

-- =====================================================
-- SECTORS
-- =====================================================

CREATE TABLE sectors (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    broad_sector TEXT,
    sub_sector TEXT,
    index_weight_pct REAL,
    market_cap_category TEXT
);

-- =====================================================
-- STOCK PRICES
-- =====================================================

CREATE TABLE stock_prices (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    date TEXT,
    open_price REAL,
    high_price REAL,
    low_price REAL,
    close_price REAL,
    volume REAL,
    adjusted_close REAL
);


CREATE TABLE IF NOT EXISTS peer_percentiles (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    company_id TEXT,

    peer_group_name TEXT,

    metric TEXT,

    value REAL,

    percentile_rank REAL,

    year TEXT

);
-- =====================================================
-- INDEXES
-- =====================================================

CREATE INDEX idx_analysis_company
ON analysis(company_id);

CREATE INDEX idx_balancesheet_company
ON balancesheet(company_id);

CREATE INDEX idx_cashflow_company
ON cashflow(company_id);

CREATE INDEX idx_documents_company
ON documents(company_id);

CREATE INDEX idx_financial_ratios_company
ON financial_ratios(company_id);

CREATE INDEX idx_market_cap_company
ON market_cap(company_id);

CREATE INDEX idx_peer_groups_company
ON peer_groups(company_id);

CREATE INDEX idx_profitandloss_company
ON profitandloss(company_id);

CREATE INDEX idx_prosandcons_company
ON prosandcons(company_id);

CREATE INDEX idx_sectors_company
ON sectors(company_id);

CREATE INDEX idx_stock_prices_company
ON stock_prices(company_id);

