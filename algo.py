import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from alpha_vantage.timeseries import TimeSeries
import datetime
import time


def generate_data(tickers, interval: str, outputsize: str, ts):
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


def getSMA(dataframe, period, on):
    """
    Calculated the Simple Moving Average.

    Args:
        dataframe: pandas dataframe.
        period: the value for moving average window.
        on: requested column (e.g: Adj close, close, etc).


    Returns:
        dataframe containing the sma as a column.
    """

    dataframe[f"sma"] = dataframe[on].rolling(period).mean()
    return dataframe


def getPervValues(dataframe, period, on):
    """
    Gets previous values of sma and requested column.

    Args:
        dataframe: pandas dataframe.
        period: the value on this many indecies in the past.
        on: requested column (e.g: Adj close, close, etc)


    Returns:
        dataframe containing the shifted values of sma and the requested column
    """
    dataframe["shifted_value"] = dataframe[on].shift(period)
    dataframe["shifted_sma"] = dataframe["sma"].shift(period)
    
    return dataframe


def apply_sma_co(dataframe, on):
    """
    Applies SMA crossover strategy

    Args:
        dataframe: pandas dataframe.
        on: requested column (e.g: Adj close, close, etc)


    Returns:
        dataframe containing the signal
    """
    def get_signal(x):
        if ((x["shifted_value"] < x["shifted_sma"]) and (x[on] > x["sma"])):
            return("BUY")
        elif ((x["shifted_value"] > x["shifted_sma"]) and (x[on] < x["sma"])):
            return("SELL")
        else:
            return("NO_ACTION")
    dataframe["signal"] = dataframe.apply(get_signal, axis=1)
    return dataframe



API_KEY = "3R9JOE98DJOXYHKJ"
ts = TimeSeries(key=API_KEY, output_format="pandas")  # initialise timeseries
TICKERS = ["IBM", "AAPL"]
# generated_data = generate_data(tickers=TICKERS, interval="5min", outputsize="full",
#                                ts=ts)  # dictionary of collected data

# for k in generated_data.keys():
#     generated_data[k].to_csv(f"data_{k}.csv")  # save as csv

df = pd.read_csv("data_AAPL.csv") # read data
df = getSMA(dataframe=df, period=10, on="Adj Close")
df = getPervValues(dataframe=df, period=1, on="Adj Close")
df = apply_sma_co(dataframe=df, on="Adj Close")
df.to_csv("test.csv")
print(df.tail())
