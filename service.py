days = 1100 #days of data to collect
days_modified = 365 #days of data to access volatility


import US_EQUITY_COLLECTION
import US_EQUITY_INI_PORTFOLIO

if True:
    US_EQUITY_INI_PORTFOLIO.initialize_portfolio()
    US_EQUITY_COLLECTION.US_EQUITY_collection(days)

import pandas as pd
return_table_modified = pd.read_csv('return_table.csv').tail(days_modified)
return_table_modified.to_csv('return_table_modified.csv')

import US_EQUITY_VAR_variance_covariance

