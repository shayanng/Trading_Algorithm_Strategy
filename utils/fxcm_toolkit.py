import fxcmpy
import socketio
import socketIO_client
import pandas as pd

def create_ohlc(fxcm_df):
    """
    Creates open, high, low, close from the collected fxcm dataframe which contains bid/ask.
    This is achieved by averaging bid and ask.

    Args:
        fxcm_df - dataframe - dataframe containing bid and ask

    Returns:
        dataframe containing aggregated open, high, low, close
    """
    fxcm_df["Open"] = (fxcm_df["bidopen"] + fxcm_df["askopen"])/2
    fxcm_df["High"] = (fxcm_df["bidhigh"] + fxcm_df["askhigh"])/2
    fxcm_df["Low"] = (fxcm_df["bidlow"] + fxcm_df["asklow"])/2
    fxcm_df["Close"] = (fxcm_df["bidclose"] + fxcm_df["askclose"])/2
    return fxcm_df[["Open", "High", "Low", "Close"]]


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

    for ticker in tickers:
        ohlc = con.get_candles(ticker, period=period, start=start, end=end)
        dataDict.update({ticker:ohlc})
    con.close()

    # check for null/nan
    for v in dataDict.values():
        if v.isnull().any().any(): 
            print("WARNING! Dataframe contains null values!")
            
    return dataDict