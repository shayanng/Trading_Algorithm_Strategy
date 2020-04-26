import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from utils import data_call as dc
from utils import tech_indicators as ti
from utils import preprocessing
from utils import trading

TICKERS = ["IBM", "AAPL", "TSLA", "NVDA"]
API_KEY = "3R9JOE98DJOXYHKJ"
ts = TimeSeries(key=API_KEY, output_format="pandas")  # initialise timeseries

# Yahoo API
# generated_data_daily = dc.generate_data(TICKERS, interval="d", n_per=90)

# AlphaVantage API
# generated_data = dc.generate_data_intraday(tickers=TICKERS, interval="5min", outputsize="full",
#                                ts=ts)  # dictionary of collected data

# for k in generated_data.keys():
#     generated_data[k].to_csv(f"./data/data_{k}.csv")  # save as csv

df = pd.read_csv("./data/data_AAPL.csv") # read data
df = ti.getSMA(dataframe=df, period=10, on="Adj Close")
df = preprocessing.getPervValues(dataframe=df, period=1, on="Adj Close")
df = trading.apply_sma_co(dataframe=df, on="Adj Close")
print(df.tail())



def stochastic(df,a,b,c):
    "function to calculate stochastic"
    df['k']=((df['c'] - df['l'].rolling(a).min())/(df['h'].rolling(a).max()-df['l'].rolling(a).min()))*100
    df['K']=df['k'].rolling(b).mean()
    df['D']=df['K'].rolling(c).mean()
    return df