import pandas as pd

companies = pd.read_excel("data/raw/companies.xlsx", header=1)

for ticker in [
    "ULTRACEMCO",
    "UNIONBANK",
    "UNITDSPR",
    "VBL",
    "VEDL",
    "WIPRO",
    "ZOMATO",
    "ZYDUSLIFE",
]:
    print(ticker, ticker in set(companies["id"]))
