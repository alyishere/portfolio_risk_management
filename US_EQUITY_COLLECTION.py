import pandas as pd
import requests
import time
from datetime import datetime as dt
import datetime
from datetime import timezone

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

def generate_return_table(price_table):
    
    price_table['date'] = price_table['date'].astype('datetime64') 

    def calculate_return(df):
        df['return'] = (df['close']/df['close'].shift(1)-1)
        return df
    price_table = price_table.groupby('ticker').apply(lambda price: calculate_return(price))
        
    return_table = price_table[['date','ticker','return']].pivot(index = 'date', columns = 'ticker', values = 'return')
    return return_table

def US_EQUITY_collection(day):
    holding_table = pd.read_csv("US_EQUITY_input.csv")
    updated_table = gather_historical_quote(holding_table,day)
    price_table = generate_price_table(updated_table)
    price_table.to_csv("US_EQUITY_price_table.csv")
    print("US_EQUITY_price_table generated.")

    return_table = generate_return_table(price_table)
    return_table.to_csv('return_table.csv')
