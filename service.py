days = 1095             #days of data to collect
days_modified = 1095    #days of data to use
loadout_set = 'ini.json'
loadout = 'default'


import pandas as pd
import numpy as np
import US_EQUITY_COLLECTION
import US_EQUITY_INI_PORTFOLIO

if True:
    US_EQUITY_INI_PORTFOLIO.initialize_portfolio(loadout = loadout,file = loadout_set)
    US_EQUITY_COLLECTION.US_EQUITY_collection(days)

return_table_modified = pd.read_csv('return_table.csv').tail(min(len(pd.read_csv("return_table.csv")),int(days_modified * 252/365)) - 1)
return_table_modified.to_csv('return_table_modified.csv')

print("Days of data collected: " + str(days_modified))
print("Days of data used: " + str(days_modified))

import US_EQUITY_VAR

def var_cvar(alpha = 0.05, h = 1):
    list = np.array([
        round(US_EQUITY_VAR.VAR_VCA(alpha = alpha, h = h),6),
        round(US_EQUITY_VAR.VAR_MCS(alpha = alpha, h = h),6),
        round(US_EQUITY_VAR.VAR_HSA(alpha = alpha, h = h),6),
        round(US_EQUITY_VAR.CVAR_parametric(alpha = alpha, h = h),6),
        round(US_EQUITY_VAR.CVAR_historical(alpha = alpha, h = h),6)
    ])
    return list

US_EQUITY_VAR.print_parametric_input()
US_EQUITY_VAR.normality_check()

varcvar_df = pd.DataFrame(index=["VAR Parametric","VAR Monte Carlo","VAR Historical Simulation","CVAR Parametric","CVAR Historical Simulation"])
varcvar_df["a0.05h1"] = var_cvar(alpha = 0.05, h = 1)
varcvar_df["a0.05h7"] = var_cvar(alpha = 0.05, h = 7)
varcvar_df["a0.05h14"] = var_cvar(alpha = 0.05, h = 14)
varcvar_df["a0.01h1"] = var_cvar(alpha = 0.01, h = 1)
varcvar_df["a0.01h7"] = var_cvar(alpha = 0.01, h = 7)
varcvar_df["a0.01h14"] = var_cvar(alpha = 0.01, h = 14)
varcvar_df["a0.001h1"] = var_cvar(alpha = 0.001, h = 1)
varcvar_df["a0.001h7"] = var_cvar(alpha = 0.001, h = 7)
varcvar_df["a0.001h14"] = var_cvar(alpha = 0.001, h = 14)
print("\nVAR/CVAR\n",varcvar_df)

varcvar_dollar_df = varcvar_df * US_EQUITY_VAR.actual_investment
print("\nVAR/CVAR ($)\n",varcvar_dollar_df)