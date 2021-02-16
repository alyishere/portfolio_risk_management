import json
setting = json.load(open('setting.json'))

days = setting['days']             
days_modified = setting['days_modified']  
loadout_set = setting['loadout_set']  
loadout = setting['loadout']  
setup = bool(setting['setup'])

print('Setting loaded.')

import datetime
output_file = "output/" + loadout+"_"+datetime.datetime.now().strftime("%Y%m%d_%H%M%S")+".txt"
import pandas as pd
import numpy as np
import US_EQUITY_COLLECTION
import US_EQUITY_INI_PORTFOLIO
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

if setup:
    US_EQUITY_INI_PORTFOLIO.initialize_portfolio(loadout = loadout,file = loadout_set)
    US_EQUITY_COLLECTION.US_EQUITY_collection(days)

return_table_modified = pd.read_csv('return_table.csv').tail(min(len(pd.read_csv("return_table.csv")),int(days_modified * 252/365)) - 1)
return_table_modified.to_csv('return_table_modified.csv')

import os
if not os.path.exists('output'):
    os.makedirs('output')

File_1 = open(output_file,"a")

File_1.write("File Loaded: \t\t\t" + loadout_set + "\tPortfolio: \t" + loadout)
File_1.write("\nDays of data collected: \t" + str(days_modified))
File_1.write("\nDays of data used: \t\t" + str(days_modified))
File_1.write("\nData up to: \t\t\t" + str(return_table_modified['date'].max()))
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
varcvar_df.to_csv('varcvar.csv')
File_1.write("\nVAR/CVAR\n")
File_1.write(str(varcvar_df))
File_1.write("\n")

varcvar_dollar_df = varcvar_df * US_EQUITY_VAR.actual_investment
varcvar_dollar_df.to_csv('varcvar_dollar.csv')
File_1.write("\nVAR/CVAR ($)\n")
File_1.write(str(varcvar_dollar_df))
File_1.close()

print('VAR/CVAR info saved.')