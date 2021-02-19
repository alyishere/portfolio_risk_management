import pandas as pd
import time
from datetime import datetime as dt
import datetime
import yfinance as yf
import json
import numpy as np
import os
import random

if not os.path.exists('cache'):
    os.makedirs('cache')

def read_load_out(loadout = 'default', file = 'ini.json'):
    ini = json.load(open(file))
    portfolio_json = ini[loadout]
    type = portfolio_json['type']
    #print("\nFile Loaded: \t\t",file,"\nPortfolio Loaded: \t",loadout)
    if type == 'weight':
        return (type,list(portfolio_json['ticker'].keys()),np.array(list(portfolio_json['ticker'].values())),portfolio_json['initial_investment'])
    if type == 'share':
        return (type,list(portfolio_json['ticker'].keys()),np.array(list(portfolio_json['ticker'].values())))

def generate_ticker_list(tickers):
    ticker_str = ""
    for i in tickers:
        ticker_str = ticker_str + " " + i 
    ticker_list = ticker_str[1:]
    return ticker_list

def collect_data(days, ticker_list, orginal_list):

    end_date = dt.today()
    start_date = end_date - datetime.timedelta(days = days + 2)
    print("Collecting Data: (Please restart if unable to complete)")
    
    ## I stopped using yf.download() since Yahoo Finance has been interrupting mass data scrapping. yf.Ticker() & history is a much stabler in comparision. 
    # data = yf.download(ticker_list, start=start_date.strftime("%Y-%m-%d"), end = end_date.strftime("%Y-%m-%d"),threads= False)
    # data.fillna(method="ffill", inplace = True)
    # data.dropna(inplace = True)
    # price_table = data['Adj Close'][orginal_list]

    ## The following is the looping yf.Ticker() & history approach.
    dfs = []
    for i in orginal_list:
        ticker = yf.Ticker(i)
        rnd_sec = random.randrange(5, 10) # throttling collection speed
        #print('Sleeping for '+str(rnd_sec)+' secondes...')
        time.sleep(rnd_sec)
        df_ticker = ticker.history(start=start_date.strftime("%Y-%m-%d"), end = end_date.strftime("%Y-%m-%d"))['Close']
        dfs.append(df_ticker.rename(i))

    data = pd.concat(dfs, axis=1)
    data.fillna(method="ffill", inplace = True)
    data.dropna(inplace = True)
    price_table = data[orginal_list]

    return_table = (price_table/price_table.shift(1)-1)
    return_table.fillna(0, inplace = True)
    return_table = return_table.iloc[1:]
    
    price_table.to_csv('cache/price_table.csv')
    return_table.to_csv('cache/return_table.csv')
    return_table.to_csv('cache/return_table_modified.csv')
    
    print("price_table generated.")
    print("return_table generated.")
    return [price_table, return_table]

def initialize_portfolio(loadout = 'default',file = 'ini.json',days = 365):

    portfolio = read_load_out(loadout,file)
    load_out_type = portfolio[0] 
    tickers = portfolio[1]
    weights = portfolio[2]
    shares = portfolio[2]
    initial_investment = 0
    if load_out_type == 'weight':
        initial_investment = portfolio[3]

    ticker_list = generate_ticker_list(tickers)
    data_list = collect_data(days, ticker_list, tickers)

    current_quote_df = pd.DataFrame(data_list[0].iloc[-1]).reset_index()

    current_quote_df.columns = ['TICKER','CURRENT_QUOTE']

    if load_out_type == 'weight':
        current_quote_df['TARGET_WEIGHT'] = weights
        current_quote_df['TARGET_ALLOCATION'] = weights*initial_investment
        current_quote_df['ACTUAL_SHARE'] = current_quote_df['TARGET_ALLOCATION']/current_quote_df['CURRENT_QUOTE']
        current_quote_df['ACTUAL_SHARE'] = current_quote_df['ACTUAL_SHARE'].astype('int')
    elif load_out_type == 'share':
        current_quote_df['ACTUAL_SHARE'] = shares

    current_quote_df['ACTUAL_ALLOCATION'] = current_quote_df['ACTUAL_SHARE'] * current_quote_df['CURRENT_QUOTE']
    current_quote_df['ACTUAL_WEIGHT'] = current_quote_df['ACTUAL_ALLOCATION']/current_quote_df['ACTUAL_ALLOCATION'].sum()
    
    current_quote_df.to_csv('cache/portfolio.csv')

    print('Portfolio initialized.')
