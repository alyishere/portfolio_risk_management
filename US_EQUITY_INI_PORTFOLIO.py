import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime as dt
import datetime
from datetime import timezone
import json

def read_load_out(loadout = 'default', file = 'ini.json'):
    ini = json.load(open(file))
    portfolio_json = ini[loadout]
    type = portfolio_json['type']
    if type == 'weight':
        return (type,list(portfolio_json['ticker'].keys()),np.array(list(portfolio_json['ticker'].values())),portfolio_json['initial_investment'])
    if type == 'share':
        return (type,list(portfolio_json['ticker'].keys()),np.array(list(portfolio_json['ticker'].values())))

def generate_ticker_list(tickers):
    ticker_str = ""
    for i in tickers:
        ticker_str = ticker_str + "," + i 
    ticker_list = ticker_str[1:]
    return ticker_list

def generate_current_quote(ticker_list):
    token = open('tradier_token.txt','r').read()
    response = requests.get('https://sandbox.tradier.com/v1/markets/quotes',
        params={'symbols': ticker_list, 'greeks': 'false'},
        headers={'Authorization': 'Bearer '+token, 'Accept': 'application/json'}
    )
    json_response = response.json()
    current_quote_df = pd.DataFrame(json_response['quotes']['quote'])[['symbol','last']].rename({'symbol':'TICKER','last':'CURRENT_QUOTE'},axis = 1).drop_duplicates() 
    return current_quote_df

def initialize_portfolio(loadout = 'default',file = 'ini.json'):

    portfolio = read_load_out(loadout,file)
    load_out_type = portfolio[0] 
    tickers = portfolio[1]
    weights = portfolio[2]
    shares = portfolio[2]
    initial_investment = 0
    if load_out_type == 'weight':
        initial_investment = portfolio[3]

    current_quote_df = generate_current_quote(generate_ticker_list(tickers))

    if load_out_type == 'weight':
        current_quote_df['TARGET_WEIGHT'] = weights
        current_quote_df['TARGET_ALLOCATION'] = weights*initial_investment
        current_quote_df['ACTUAL_SHARE'] = current_quote_df['TARGET_ALLOCATION']/current_quote_df['CURRENT_QUOTE']
        current_quote_df['ACTUAL_SHARE'] = current_quote_df['ACTUAL_SHARE'].astype('int')
    elif load_out_type == 'share':
        current_quote_df['ACTUAL_SHARE'] = shares

    current_quote_df['ACTUAL_ALLOCATION'] = current_quote_df['ACTUAL_SHARE'] * current_quote_df['CURRENT_QUOTE']
    current_quote_df['ACTUAL_WEIGHT'] = current_quote_df['ACTUAL_ALLOCATION']/current_quote_df['ACTUAL_ALLOCATION'].sum()
    
    current_quote_df.to_csv('US_EQUITY_input.csv')