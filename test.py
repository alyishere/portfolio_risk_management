import pandas as pd
import requests
import time
from datetime import datetime as dt
import datetime
from datetime import timezone


def initiate_portfolio_df():
    df = pd.read_csv('input.csv')
    return df[['TICKER','TYPE','HOLDING','REGION']]

def generate_ticker_list(portfolio_df):
    ticker_str = ""
    for i in portfolio_df['TICKER']:
        ticker_str = ticker_str + "," + i 
        if len(i) > 10:
            ticker_str = ticker_str + "," + i[:-15] 
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

def combine_current_quote(portfolio_df,current_quote_df):
    combined_df = pd.merge(portfolio_df,current_quote_df,how="inner",on="TICKER")
    combined_df['MARKET_VALUE'] = combined_df['HOLDING'] * combined_df['CURRENT_QUOTE'] 
    return combined_df

def generate_portfolio_view1():
    portfolio_df = initiate_portfolio_df()
    current_quote_df = generate_current_quote(generate_ticker_list(portfolio_df))
    combined_df = combine_current_quote(portfolio_df,current_quote_df)
    return combined_df[['TICKER','TYPE','REGION','HOLDING','CURRENT_QUOTE','MARKET_VALUE']]

#print(generate_portfolio_view1())

end_date = dt.today()#.strftime("%Y-%m-%d")
start_date = end_date - datetime.timedelta(days = 730)
print(end_date)
print(start_date)
token = open('tradier_token.txt','r').read()
#def gather_historical_quote(orders):
def request_historicals(ticker,start_date,end_date):
    response = requests.get('https://sandbox.tradier.com/v1/markets/history',
        params={'symbol': ticker, 'interval': 'daily', 'start': start_date.strftime("%Y-%m-%d"), 'end': end_date.strftime("%Y-%m-%d")},
        headers={'Authorization': 'Bearer '+token, 'Accept': 'application/json'}
    )
    json_response = response.json()
    return json_response['history']['day']
holding_table['historical_quote'] = holding_table.apply(lambda ticker: request_historicals(ticker['Ticker'],ticker['Date']),axis = 1)