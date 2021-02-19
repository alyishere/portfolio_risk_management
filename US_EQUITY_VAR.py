import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import random
import scipy
#import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


holding_table = pd.read_csv("cache/portfolio.csv").set_index('TICKER').drop("Unnamed: 0",axis = 1)
return_table = pd.read_csv('cache/return_table_modified.csv').drop('Unnamed: 0',axis = 1).set_index('Date')

all_return = (return_table.values*holding_table['ACTUAL_WEIGHT'].values).sum(axis=1)

cov_matrix = return_table.cov()
corr_matrix = return_table.corr()
avg_return = return_table.mean()
weight = holding_table['ACTUAL_WEIGHT']

portfolio_avg_return = avg_return.dot(holding_table['ACTUAL_WEIGHT'])
portfolio_stdev = np.sqrt(weight.T.dot(cov_matrix).dot(weight))

actual_investment = holding_table['ACTUAL_ALLOCATION'].sum()

properties = pd.DataFrame(avg_return).rename({0:'Daily Return'},axis = 1)
properties['Annualized Return'] = ((avg_return+1)**252-1)
properties['Daily Stdev'] = return_table.std()
properties['Annualized Stdev'] = return_table.std()*np.sqrt(252)
properties['Annual Sharpe Ratio'] = properties['Annualized Return']/properties['Annualized Stdev']

output_properties = properties.to_string(formatters={
    'Daily Return': '{:,.2%}'.format,
    'Annualized Return': '{:,.2%}'.format,
    'Daily Stdev': '{:,.2%}'.format,
    'Annualized Stdev': '{:,.2%}'.format,
    'Annual Sharpe Ratio': '{:,.2f}'.format
})

# avg_return_investment = actual_investment * (1 + portfolio_avg_return)
# stdev_investment = actual_investment * portfolio_stdev

def parametric_input():
    output_str = ''
    output_str += "\nHolding Table\n"
    output_str += str(holding_table)
    output_str += "\nActual Initial Investment: \t" + str(round(actual_investment,2))
    output_str += "\nPortfolio Average Return: \t" + str(round(100*portfolio_avg_return,2)) + "%\n*Annualized: \t\t\t" + str(round(100*((portfolio_avg_return+1)**252-1),2))+'%'
    output_str += "\nPortfolio stdev: \t\t" + str(round(100*portfolio_stdev,2)) + "%\n*Annualized: \t\t\t" + str(round(100*(portfolio_stdev * np.sqrt(252)),2))+'%'
    output_str += "\nPortfolio SR (a): \t\t" + str(round(((portfolio_avg_return+1)**252-1)/(portfolio_stdev * np.sqrt(252)),2))
    output_str += "\n" + str(output_properties)
    output_str += "\n\nCorrelation Matrix\n"
    output_str += str(corr_matrix)
    output_str += "\n\n"
    return output_str

def normality_check():
    #check whether the returns fell under normal distribution

    import os
    if not os.path.exists('normality check charts'):
        os.makedirs('normality check charts')

    for stock in return_table.columns:
        return_table[stock].hist(bins=40, density=True,histtype="stepfilled",alpha=0.5)
        x = np.linspace(portfolio_avg_return - 3 * portfolio_stdev, portfolio_avg_return + 3 * portfolio_stdev,100)
        plt.plot(x, scipy.stats.norm.pdf(x, portfolio_avg_return, portfolio_stdev), "r")
        plt.title(stock + " returns (binned) vs. normal distribution")

        plt.savefig('normality check charts/' + stock + '.jpg',dpi = 300)
        plt.clf()

def normality_check_portfolio():
    #check whether the returns fell under normal distribution
    import os
    if not os.path.exists('normality check charts'):
        os.makedirs('normality check charts')

    pd.DataFrame(all_return).hist(bins=40, density=True,histtype="stepfilled",alpha=0.5)
    x = np.linspace(portfolio_avg_return - 3 * portfolio_stdev, portfolio_avg_return + 3 * portfolio_stdev,100)
    plt.plot(x, scipy.stats.norm.pdf(x, portfolio_avg_return, portfolio_stdev), "r")
    plt.title("Portfolio returns (binned) vs. normal distribution")

    plt.savefig('normality check charts/portfolio.jpg',dpi = 300)
    plt.clf()

## Variance-Covariance Approach (parametric)
def VAR_VCA(alpha, portfolio_avg_return = portfolio_avg_return, portfolio_stdev = portfolio_stdev, h = 1):
    portfolio_stdev_h = portfolio_stdev * np.sqrt(h)
    return norm.ppf(1 - alpha) * portfolio_stdev_h - portfolio_avg_return

## Monte Carlo Simulation (parametric)
def VAR_MCS(alpha, portfolio_avg_return = portfolio_avg_return, portfolio_stdev = portfolio_stdev, n_sim = 100000, h = 1):
    sim_returns = np.random.normal(portfolio_avg_return, portfolio_stdev, n_sim)
    sim_VAR = np.percentile(sim_returns, alpha * 100)
    return -sim_VAR * np.sqrt(h)

## Historical Simulation Approach 
def VAR_HSA(alpha, all_return = all_return, h = 1, method = "simulation", n_sim = 100000):
    var = 0
    if method == "simple":
        historic_var_percent = np.percentile(all_return, alpha * 100, interpolation="lower")
        var = -historic_var_percent * np.sqrt(h)
    elif method == "simulation":
        def random_list(choices, size):
            return np.array([random.choice(choices) for _ in range(size)])
        random_return = np.array([1] * n_sim)
        while h > 0:
            random_return1 = (1 + random_list(all_return,n_sim))
            random_return = random_return * random_return1
            h = h - 1
        random_return = random_return - 1
        var = -np.percentile(random_return, alpha * 100, interpolation="lower")
    return var

## CVAR, Assuming Normal Distribution
def CVAR_parametric(alpha, portfolio_avg_return = portfolio_avg_return, portfolio_stdev = portfolio_stdev, h = 1):
    portfolio_stdev_h = portfolio_stdev * np.sqrt(h)
    return alpha**-1 * norm.pdf(norm.ppf(alpha)) * portfolio_stdev_h - portfolio_avg_return

## CVAR, Using Historical Data
def CVAR_historical(alpha, all_return = all_return, n_sim = 100000, h = 1):
    def random_list(choices, size):
        return np.array([random.choice(choices) for _ in range(size)])
    random_return = np.array([1] * n_sim)
    while h > 0:
        random_return1 = (1 + random_list(all_return,n_sim))
        random_return = random_return * random_return1
        h = h - 1
    random_return = random_return - 1
    cut_off = np.percentile(random_return, alpha * 100, interpolation="lower")
    return -random_return[random_return<=cut_off].mean()


    

