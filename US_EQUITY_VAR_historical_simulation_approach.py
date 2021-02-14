import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

return_table = pd.read_csv('return_table_modified.csv').drop('Unnamed: 0',axis = 1).set_index('date')

holding_table = pd.read_csv("US_EQUITY_input.csv").set_index('TICKER').drop("Unnamed: 0",axis = 1)
actual_investment = holding_table['ACTUAL_ALLOCATION'].sum()
all_return = (return_table.values*holding_table['ACTUAL_WEIGHT'].values).sum(axis=1)

## Historical Simulation Approach
def VAR(conf_level, all_return, investment, day, method = "simple"):
    var = 0
    if method == "simple":
        historic_var_percent = np.percentile(all_return, conf_level * 100, interpolation="lower")
        var = -(historic_var_percent * investment) * np.sqrt(day)
    elif method == "simulation":
        None

    return round(var,4)

def print_out_var(method = "simple"):
    print('\n')
    if method == "simple":
        print('Historical Simulation Approach (simple)')
    print("1 day VaR \t@ 95% confidence: \t" + str(VAR(0.05,all_return,actual_investment,1, method = method)))
    print("7 day VaR \t@ 95% confidence: \t" + str(VAR(0.05,all_return,actual_investment,7, method = method)))
    print("14 day VaR \t@ 95% confidence: \t" + str(VAR(0.05,all_return,actual_investment,14, method = method)))
    print("1 day VaR \t@ 99% confidence: \t" + str(VAR(0.01,all_return,actual_investment,1, method = method)))
    print("7 day VaR \t@ 99% confidence: \t" + str(VAR(0.01,all_return,actual_investment,7, method = method)))
    print("14 day VaR \t@ 99% confidence: \t" + str(VAR(0.01,all_return,actual_investment,14, method = method)))
    print("1 day VaR \t@ 99.9% confidence: \t" + str(VAR(0.001,all_return,actual_investment,1, method = method)))
    print("7 day VaR \t@ 99.9% confidence: \t" + str(VAR(0.001,all_return,actual_investment,7, method = method)))
    print("14 day VaR \t@ 99.9% confidence: \t" + str(VAR(0.001,all_return,actual_investment,14, method = method)))
    print('\n')

def print_out_var_chart(method = "simple"):
    var_array_95 = []
    var_array_99 = []
    var_array_999 = []

    num_days = int(14)

    var95_1d = VAR(0.05, all_return, actual_investment, 1, method = method)
    var99_1d = VAR(0.01, all_return, actual_investment, 1, method = method)
    var999_1d = VAR(0.001, all_return, actual_investment, 1, method = method)

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
    if method == "simple":
        plt.savefig("VAR(HSA-simple).jpg",dpi = 300)
    elif method == "simulation":
        None
    plt.clf()
    #plt.show()
