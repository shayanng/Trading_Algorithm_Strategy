from alpha_vantage.timeseries import TimeSeries
import pandas_datareader.data as web
import pandas as pd
import datetime
import time

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

## FXCM API
def get_fxcm_data(token, tickers, period, start, end):
    """
    Collects market data for a list of instruments from the FXCM API.

    Args:
        token: FXCM API Token.
        tickers: List of tickers.
        period: string - Time interval between data points.
        start: datetime object - start date
        end: datetime object - end date

    Returns:
        dataDict: Dictionary with Keys as Ticker names and values as dataframe
    """
    dataDict = {}
    con = fxcmpy.fxcmpy(access_token=token, log_level='error', server='demo', log_file='log.txt') #init connection

    for ticker in TICKERS:
        ohlc = con.get_candles(ticker, period=period, start=start, end=end)
        dataDict.update({ticker:ohlc})
    con.close()
    return dataDict