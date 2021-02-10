days = 1100 #days of data to collect
days_modified = 365 #days of data to access volatility


import US_EQUITY_COLLECTION
import US_EQUITY_INI_PORTFOLIO

if False:
    US_EQUITY_INI_PORTFOLIO.initialize_portfolio()
if False:
    US_EQUITY_COLLECTION.US_EQUITY_collection(days)

import pandas as pd
return_table_modified = pd.read_csv('return_table.csv').tail(int(days_modified * 254/365))
return_table_modified.to_csv('return_table_modified.csv')
print("Days of data used: " + str(days_modified))

import US_EQUITY_VAR_variance_covariance_approach
US_EQUITY_VAR_variance_covariance_approach.print_out_var()
US_EQUITY_VAR_variance_covariance_approach.print_out_var_chart()
US_EQUITY_VAR_variance_covariance_approach.normality_check()

import US_EQUITY_VAR_historical_simulation_approach
US_EQUITY_VAR_historical_simulation_approach.print_out_var()
US_EQUITY_VAR_historical_simulation_approach.print_out_var_chart()