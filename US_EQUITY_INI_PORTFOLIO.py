import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime as dt
import datetime
from datetime import timezone

tickers = ['GME','MSFT', 'SPY', 'TSLA']
weights = np.array([.25, .3, .15, .3])
initial_investment = 1000000

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

def initialize_portfolio():
    current_quote_df = generate_current_quote(generate_ticker_list(tickers))
    current_quote_df['TARGET_WEIGHT'] = weights
    current_quote_df['TARGET_ALLOCATION'] = weights*initial_investment
    current_quote_df['ACTUAL_SHARE'] = current_quote_df['TARGET_ALLOCATION']/current_quote_df['CURRENT_QUOTE']
    current_quote_df['ACTUAL_SHARE'] = current_quote_df['ACTUAL_SHARE'].astype('int')
    current_quote_df['ACTUAL_ALLOCATION'] = current_quote_df['ACTUAL_SHARE'] * current_quote_df['CURRENT_QUOTE']
    current_quote_df['ACTUAL_WEIGHT'] = current_quote_df['ACTUAL_ALLOCATION']/current_quote_df['ACTUAL_ALLOCATION'].sum()
    current_quote_df.to_csv('US_EQUITY_input.csv')