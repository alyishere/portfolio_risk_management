import json
setting = json.load(open('setting.json'))

days = setting['days']             
days_modified = setting['days_modified']  
loadout_set = setting['loadout_set']  
loadout = setting['loadout']  
setup = bool(setting['setup']=='True')

print('Setting loaded.')

import datetime
import pandas as pd
import numpy as np
import US_EQUITY_COLLECTION

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

import os
if not os.path.exists('output'):
    os.makedirs('output')
if not os.path.exists('cache'):
    os.makedirs('cache')

if setup:
    US_EQUITY_COLLECTION.initialize_portfolio(loadout = loadout, file = loadout_set, days = days)

return_table_modified = pd.read_csv('cache/return_table.csv').tail(min(len(pd.read_csv("cache/return_table.csv")),int(days_modified * 252/365)) - 1)
return_table_modified.to_csv('cache/return_table_modified.csv')

output_file = "output/" + loadout+"_"+datetime.datetime.now().strftime("%Y%m%d_%H%M%S")+".txt"
File_1 = open(output_file,"a")

File_1.write("File Loaded: \t\t\t" + loadout_set + "\tPortfolio: \t" + loadout)
File_1.write("\nDays of data collected: \t" + str(days_modified))
File_1.write("\nDays of data used: \t\t" + str(days_modified))
File_1.write("\nData up to: \t\t\t" + str(return_table_modified['Date'].max()))
File_1.write("\n")

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

File_1.write(US_EQUITY_VAR.parametric_input())
print('Parametric info saved.')
US_EQUITY_VAR.normality_check()
US_EQUITY_VAR.normality_check_portfolio()


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

varcvar_df.to_csv('cache/varcvar.csv')
File_1.write("\nVAR/CVAR\n")
File_1.write(str(varcvar_df))
File_1.write("\n")

varcvar_dollar_df = varcvar_df * US_EQUITY_VAR.actual_investment

varcvar_dollar_df.to_csv('cache/varcvar_dollar.csv')
File_1.write("\nVAR/CVAR ($)\n")
File_1.write(str(varcvar_dollar_df))
File_1.close()

print('VAR/CVAR info saved.')