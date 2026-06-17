import pandas as pd

companies = pd.read_excel("data/raw/companies.xlsx", header=1)

print(companies["id"].tail(20))

print(companies.shape)
