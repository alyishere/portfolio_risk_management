import US_EQUITY_COLLECTION
import US_EQUITY_INI_PORTFOLIO
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# def generate_return_table(price_table):
    
#     price_table['date'] = price_table['date'].astype('datetime64') 

#     def calculate_return(df):
#         df['return'] = (df['close']/df['close'].shift(1)-1)
#         return df
#     price_table = price_table.groupby('ticker').apply(lambda price: calculate_return(price))
        
#     return_table = price_table[['date','ticker','return']].pivot(index = 'date', columns = 'ticker', values = 'return')
#     return return_table

# price_table = pd.read_csv("US_EQUITY_price_table.csv")
# return_table = generate_return_table(price_table)
# return_table.to_csv('return_table.csv')

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

# print(holding_table)
# print("\nActual Initial Investment\n", actual_investment)
# print("\nCovariance Matrix\n", cov_matrix)
# print("\nAverage Return\n", avg_return)
# print("\nPortfolio Weight\n", weight)
# print("\nPortfolio Average Return\n", portfolio_avg_return)
# print("\nPortfolio stdev\n", portfolio_stdev)
# print("\nPortfolio Average Return (in $)\n", avg_return_investment)
# print("\nPortfolio stdev (in $)\n", stdev_investment)

## Variance-Covariance Approach
def VAR(conf_level, avg_return_investment, stdev_investment, investment,day):
    cutoff = norm.ppf(conf_level, avg_return_investment, stdev_investment)
    var = (investment - cutoff) * np.sqrt(day)
    return round(var,4)

print('\n')
print("1 day VaR @ 95% confidence: \t" + str(VAR(0.05,avg_return_investment,stdev_investment,actual_investment,1)))
print("7 day VaR @ 95% confidence: \t" + str(VAR(0.05,avg_return_investment,stdev_investment,actual_investment,7)))
print("14 day VaR @ 95% confidence: \t" + str(VAR(0.05,avg_return_investment,stdev_investment,actual_investment,14)))
print("1 day VaR @ 99% confidence: \t" + str(VAR(0.01,avg_return_investment,stdev_investment,actual_investment,1)))
print("7 day VaR @ 99% confidence: \t" + str(VAR(0.01,avg_return_investment,stdev_investment,actual_investment,7)))
print("14 day VaR @ 99% confidence: \t" + str(VAR(0.01,avg_return_investment,stdev_investment,actual_investment,14)))
print("1 day VaR @ 99.9% confidence: \t" + str(VAR(0.001,avg_return_investment,stdev_investment,actual_investment,1)))
print("7 day VaR @ 99.9% confidence: \t" + str(VAR(0.001,avg_return_investment,stdev_investment,actual_investment,7)))
print("14 day VaR @ 99.9% confidence: \t" + str(VAR(0.001,avg_return_investment,stdev_investment,actual_investment,14)))


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
