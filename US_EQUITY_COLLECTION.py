import pandas as pd
import requests
import time
from datetime import datetime as dt
import datetime
from datetime import timezone

def initiate_portfolio_df():
    df = pd.read_csv('US_EQUITY_input.csv')
    return df[['TICKER','TYPE','HOLDING','REGION']]

def generate_ticker_list(portfolio_df):
    ticker_str = ""
    for i in portfolio_df['TICKER']:
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

def combine_current_quote(portfolio_df,current_quote_df):
    combined_df = pd.merge(portfolio_df,current_quote_df,how="inner",on="TICKER")
    combined_df['MARKET_VALUE'] = combined_df['HOLDING'] * combined_df['CURRENT_QUOTE'] 
    return combined_df

def generate_portfolio_view1():
    portfolio_df = initiate_portfolio_df()
    current_quote_df = generate_current_quote(generate_ticker_list(portfolio_df))
    combined_df = combine_current_quote(portfolio_df,current_quote_df)
    return combined_df[['TICKER','TYPE','REGION','HOLDING','CURRENT_QUOTE','MARKET_VALUE']]


def gather_historical_quote(holding_table,days):

    end_date = dt.today()
    start_date = end_date - datetime.timedelta(days = days)
    token = open('tradier_token.txt','r').read()

    def request_historicals(ticker,start_date,end_date):
        response = requests.get('https://sandbox.tradier.com/v1/markets/history',
            params={'symbol': ticker, 'interval': 'daily', 'start': start_date.strftime("%Y-%m-%d"), 'end': end_date.strftime("%Y-%m-%d")},
            headers={'Authorization': 'Bearer '+token, 'Accept': 'application/json'}
        )
        json_response = response.json()
        return json_response['history']['day']
    holding_table['historical_quote'] = holding_table.apply(lambda ticker: request_historicals(ticker['TICKER'],start_date,end_date),axis = 1)
    return holding_table

def generate_price_table(df):
    import pandas as pd
    price_table = pd.DataFrame(columns=("ticker","open","high","low","close","volume"))
    for i in df.index:
        entry = df.loc[i,:]
        current_df = pd.DataFrame(entry['historical_quote'])
        current_df['ticker'] = entry['TICKER']
        price_table = pd.concat([price_table,current_df],sort=True)
    return price_table

def US_EQUITY_collection():
    holding_table = generate_portfolio_view1()
    holding_table.to_csv("US_EQUITY_holding_table.csv")
    print("US_EQUITY_holding_table generated.")

    updated_table = gather_historical_quote(holding_table,730)
    generate_price_table(updated_table).to_csv("US_EQUITY_price_table.csv")
    print("US_EQUITY_price_table generated.")