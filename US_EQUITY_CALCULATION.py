#%%
import US_EQUITY_COLLECTION
import pandas as pd
#%%
US_EQUITY_COLLECTION.US_EQUITY_collection()

#%%
price_table = pd.read_csv("US_EQUITY_price_table.csv").drop("Unnamed: 0",axis = 1)
print(price_table)

# %%
price_table['date'] = price_table['date'].astype('datetime64') 
price_table.dtypes
# %%
price_table = price_table.sort_values(["ticker","date"])
# %%

# %%
def calculate_return(df):
    df['return'] = (df['close']/df['close'].shift(1)-1)
    return df
price_table = price_table.groupby('ticker').apply(lambda price: calculate_return(price))
    
price_table    
# %%
GME_table = price_table[price_table['ticker']=='GME']
# %%
GME_table.tail(30).plot(x='date',y='close')
# %%
GME_table.tail(30).plot(x='date',y='return')
# %%
GME_table.tail(30).plot(x='date',y='return',kind = 'hist')
# %%
