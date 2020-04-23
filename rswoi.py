from alpha_vantage.timeseries import TimeSeries
import datetime
import time
import pandas as pd


def generate_data(tickers, interval:str, outputsize:str, ts):
    """
    Collects data for a set of tickers and return a dictionary,
    with keys being ticker name and values being pandas dataframe corresponding to the key.
    """
    
    ohlc_intraday = {}
    attempts = 0
    drop = []
    while len(tickers) != 0 and attempts <= 5:
        tickers = [j for j in tickers if j not in drop]
        for i in range(len(tickers)):
            try:
                ohlc_intraday[tickers[i]] = ts.get_intraday(symbol=tickers[i], interval=interval,
                                                            outputsize=outputsize)[0]
                ohlc_intraday[tickers[i]].columns = ["Open", "High", "Low", "Adj Close", "Volume"]
                drop.append(tickers[i])
            except Exception as e:
                print(e)
                print(tickers[i], " :failed to fetch data...retrying")
                continue
        attempts += 1
    return ohlc_intraday


API_KEY = "3R9JOE98DJOXYHKJ"
ts = TimeSeries(key=API_KEY, output_format = "pandas") #initialise timeseries
TICKERS = ["IBM", "AAPL"]
generated_data = generate_data(tickers=TICKERS, interval="5min", outputsize="full", ts=ts) # dictionary of collected data

for k in generated_data.keys():
    generated_data[k].to_csv(f"data_{k}.csv") # save as csv
    
    