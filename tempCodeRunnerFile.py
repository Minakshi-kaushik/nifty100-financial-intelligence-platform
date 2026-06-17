from src.etl.normaliser import normalize_ticker, normalize_year

print(normalize_ticker(" abb "))
# ABB

print(normalize_year("Dec 2012"))
# 2012-12

print(normalize_year("Mar 2014"))
# 2014-03

print(normalize_year("Mar-13"))
# 2013-03

print(normalize_year("2024"))
# 2024
