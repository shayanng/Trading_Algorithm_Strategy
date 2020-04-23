from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import time
import sys
import statsmodels.api as sm
plt.style.use("ggplot")


ticker = ["IBM", "AAPL"]


API_key = "3R9JOE98DJOXYHKJ"
ts = TimeSeries(key = API_key, output_format = "pandas")


def generate_data(tickers, interval:str, outputsize:str):
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
    return


jj = generate_data(ticker, "5min", "full")

# tickers = ohlc_intraday.keys()

################################Data Extraction####################################




# nvda_5mins = ohlc_intraday["NVDA"]
# msft_5mins = ohlc_intraday["MSFT"]
# pd.to_csv