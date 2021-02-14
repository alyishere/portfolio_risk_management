#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

holding_table = pd.read_csv("US_EQUITY_input.csv").set_index('TICKER').drop("Unnamed: 0",axis = 1)
return_table = pd.read_csv('return_table_modified.csv').drop('Unnamed: 0',axis = 1)

cov_matrix = return_table.cov()
avg_return = return_table.mean()
weight = holding_table['ACTUAL_WEIGHT']

portfolio_avg_return = avg_return.dot(holding_table['ACTUAL_WEIGHT'])
portfolio_stdev = np.sqrt(weight.T.dot(cov_matrix).dot(weight))

actual_investment = holding_table['ACTUAL_ALLOCATION'].sum()

def VAR(conf_level, portfolio_avg_return, portfolio_stdev, actual_investment, n_sim, day):
  n_sim = 1000000
  sim_returns = np.random.normal(portfolio_avg_return, portfolio_stdev, n_sim)
  SimVAR = actual_investment*np.percentile(sim_returns, conf_level * 100)
  return round(-SimVAR * np.sqrt(day),4)

def print_out_var():
    print('\n')
    print('Monte Carlo Simulation')
    print("1 day VaR \t@ 95% confidence: \t" + str(VAR(0.05,portfolio_avg_return,portfolio_stdev,actual_investment,10000,1)))
    print("7 day VaR \t@ 95% confidence: \t" + str(VAR(0.05,portfolio_avg_return,portfolio_stdev,actual_investment,10000,7)))
    print("14 day VaR \t@ 95% confidence: \t" + str(VAR(0.05,portfolio_avg_return,portfolio_stdev,actual_investment,10000,14)))
    print("1 day VaR \t@ 99% confidence: \t" + str(VAR(0.01,portfolio_avg_return,portfolio_stdev,actual_investment,10000,1)))
    print("7 day VaR \t@ 99% confidence: \t" + str(VAR(0.01,portfolio_avg_return,portfolio_stdev,actual_investment,10000,7)))
    print("14 day VaR \t@ 99% confidence: \t" + str(VAR(0.01,portfolio_avg_return,portfolio_stdev,actual_investment,10000,14)))
    print("1 day VaR \t@ 99.9% confidence: \t" + str(VAR(0.001,portfolio_avg_return,portfolio_stdev,actual_investment,10000,1)))
    print("7 day VaR \t@ 99.9% confidence: \t" + str(VAR(0.001,portfolio_avg_return,portfolio_stdev,actual_investment,10000,7)))
    print("14 day VaR \t@ 99.9% confidence: \t" + str(VAR(0.001,portfolio_avg_return,portfolio_stdev,actual_investment,10000,14)))
    print('\n')

def print_out_var_chart():
    var_array_95 = []
    var_array_99 = []
    var_array_999 = []

    num_days = int(14)

    var95_1d = VAR(0.05,portfolio_avg_return,portfolio_stdev,actual_investment,10000,1)
    var99_1d = VAR(0.01,portfolio_avg_return,portfolio_stdev,actual_investment,10000,1)
    var999_1d = VAR(0.001,portfolio_avg_return,portfolio_stdev,actual_investment,10000,1)

    for x in range(1, num_days+1):    
        var_array_95.append(np.round(var95_1d * np.sqrt(x),2))
    for x in range(1, num_days+1):    
        var_array_99.append(np.round(var99_1d * np.sqrt(x),2))
    for x in range(1, num_days+1):    
        var_array_999.append(np.round(var999_1d * np.sqrt(x),2))

    fig, ax = plt.subplots()

    plt.xlabel("Day #")
    plt.ylabel("Max portfolio loss (USD)")
    plt.title("Max portfolio loss (VaR) over 15-day period")

    ax.plot(var_array_95, label='VAR 95', color = "r")
    ax.plot(var_array_99, label='VAR 99', color = "g")
    ax.plot(var_array_999, label='VAR 99.9', color = "b")
    legend = ax.legend(loc='upper left', fontsize='medium')

    plt.gcf().subplots_adjust(left=0.15)

    plt.savefig("VAR(MCS).jpg",dpi = 300)
    plt.clf()