from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import numpy as np
import pandas_datareader.data as web
import pandas as pd
import datetime
import time
import sys
import statsmodels.api as sm
plt.style.use("ggplot")


## generating data from YF API
def generate_data(tickers, interval:str = "d", n_per:int = 30):
    """
    Generating non-intraday Data From YF API
    """
    ohlc_per = {}
    attempt = 0
    drop = []
    while len(tickers) != 0 and attempt <= 5:
        tickers = [j for j in tickers if j not in drop]
        for i in range(len(tickers)):
            try:
                ohlc_per[tickers[i]] = web.get_data_yahoo(tickers[i], datetime.date.today()-datetime.timedelta(n_per),
                                                          datetime.date.today(), interval=interval)
                ohlc_per[tickers[i]].dropna(inplace = True)
                drop.append(tickers[i])
            except Exception as e:
                print(e)
                print(tickers[i]," :failed to fetch data... retrying")
                continue
        attempt += 1
    return ohlc_per


## generating data from Alpha vantage API (only for intraday data)
def generate_data_intraday(tickers, interval: str, outputsize: str, ts):
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


# API_KEY = "3R9JOE98DJOXYHKJ"
# ts = TimeSeries(key=API_KEY, output_format="pandas")  # initialise timeseries
# TICKERS = ["IBM", "AAPL", "TSLA", "NVDA"]
# generated_data = generate_data_intraday(tickers=TICKERS, interval="5min", outputsize="full",
#                                ts=ts)  # dictionary of collected data
#
# for k in generated_data.keys():
#     generated_data[k].to_csv(f"data_{k}.csv")  # save as csv


