import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

return_table = pd.read_csv('return_table_modified.csv').drop('Unnamed: 0',axis = 1).set_index('date')

holding_table = pd.read_csv("US_EQUITY_input.csv").set_index('TICKER').drop("Unnamed: 0",axis = 1)
actual_investment = holding_table['ACTUAL_ALLOCATION'].sum()
all_return = (return_table.values*holding_table['ACTUAL_WEIGHT'].values).sum(axis=1)

def CVAR(conf_level, all_return, investment, day):
    historic_var_percent = np.percentile(all_return, conf_level * 100, interpolation="lower")
    cvar_percent = all_return[all_return <= historic_var_percent].mean()
    var = -(cvar_percent * investment) * np.sqrt(day)
    return round(var,4)
CVAR(0.05, all_return, actual_investment, 1)


