-- Query 1
SELECT COUNT(*) FROM companies;

-- Query 2
SELECT company_name
FROM companies
LIMIT 10;

-- Query 3
SELECT company_id, sales
FROM profitandloss
ORDER BY sales DESC
LIMIT 10;

-- Query 4
SELECT company_id, net_profit
FROM profitandloss
ORDER BY net_profit DESC
LIMIT 10;

-- Query 5
SELECT company_id, total_assets
FROM balancesheet
ORDER BY total_assets DESC
LIMIT 10;

-- Query 6
SELECT company_id, net_cash_flow
FROM cashflow
ORDER BY net_cash_flow DESC
LIMIT 10;

-- Query 7
SELECT company_id, roe_percentage
FROM companies
ORDER BY roe_percentage DESC
LIMIT 10;

-- Query 8
SELECT COUNT(*)
FROM stock_prices;

-- Query 9
SELECT company_id, market_cap_crore
FROM market_cap
ORDER BY market_cap_crore DESC
LIMIT 10;

-- Query 10
SELECT company_id, broad_sector
FROM sectors
LIMIT 20;