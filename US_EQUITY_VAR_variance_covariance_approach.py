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

avg_return_investment = actual_investment * (1 + portfolio_avg_return)
stdev_investment = actual_investment * portfolio_stdev

print(holding_table)
print("\nActual Initial Investment: \t\t", round(actual_investment,4))
print("Portfolio Average Return: \t\t", round(portfolio_avg_return,6))
print("Portfolio stdev: \t\t\t", round(portfolio_stdev,6))
print("Portfolio Average Return (in $): \t", round(avg_return_investment,4))
print("Portfolio stdev (in $): \t\t", round(stdev_investment,4))
print("\nAverage Return\n", avg_return)
print("\nCovariance Matrix\n", cov_matrix)

## Variance-Covariance Approach
def VAR(conf_level, avg_return_investment, stdev_investment, investment,day):
    cutoff = norm.ppf(conf_level, avg_return_investment, stdev_investment)
    var = (investment - cutoff) * np.sqrt(day)
    return round(var,4)

def print_out_var():
    print('\n')
    print('Variance-Covariance Approach')
    print("1 day VaR \t@ 95% confidence: \t" + str(VAR(0.05,avg_return_investment,stdev_investment,actual_investment,1)))
    print("7 day VaR \t@ 95% confidence: \t" + str(VAR(0.05,avg_return_investment,stdev_investment,actual_investment,7)))
    print("14 day VaR \t@ 95% confidence: \t" + str(VAR(0.05,avg_return_investment,stdev_investment,actual_investment,14)))
    print("1 day VaR \t@ 99% confidence: \t" + str(VAR(0.01,avg_return_investment,stdev_investment,actual_investment,1)))
    print("7 day VaR \t@ 99% confidence: \t" + str(VAR(0.01,avg_return_investment,stdev_investment,actual_investment,7)))
    print("14 day VaR \t@ 99% confidence: \t" + str(VAR(0.01,avg_return_investment,stdev_investment,actual_investment,14)))
    print("1 day VaR \t@ 99.9% confidence: \t" + str(VAR(0.001,avg_return_investment,stdev_investment,actual_investment,1)))
    print("7 day VaR \t@ 99.9% confidence: \t" + str(VAR(0.001,avg_return_investment,stdev_investment,actual_investment,7)))
    print("14 day VaR \t@ 99.9% confidence: \t" + str(VAR(0.001,avg_return_investment,stdev_investment,actual_investment,14)))
    print('\n')

def print_out_var_chart():
    var_array_95 = []
    var_array_99 = []
    var_array_999 = []

    num_days = int(14)

    var95_1d = VAR(0.05, avg_return_investment, stdev_investment, actual_investment,1)
    var99_1d = VAR(0.01, avg_return_investment, stdev_investment, actual_investment,1)
    var999_1d = VAR(0.001, avg_return_investment, stdev_investment, actual_investment,1)

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

    plt.savefig("VAR(VCA).jpg",dpi = 300)
    plt.clf()
    #plt.show()

def normality_check():
    #check whether the returns fell under normal distribution
    import scipy
    import matplotlib.mlab as mlab
    import matplotlib.pyplot as plt

    import os
    if not os.path.exists('normality check charts'):
        os.makedirs('normality check charts')

    for stock in return_table.columns[1:]:
        return_table[stock].hist(bins=40, density=True,histtype="stepfilled",alpha=0.5)
        x = np.linspace(portfolio_avg_return - 3 * portfolio_stdev, portfolio_avg_return + 3 * portfolio_stdev,100)
        plt.plot(x, scipy.stats.norm.pdf(x, portfolio_avg_return, portfolio_stdev), "r")
        plt.title(stock + " returns (binned) vs. normal distribution")

        plt.savefig('normality check charts/' + stock + '.jpg',dpi = 300)
        plt.clf()
