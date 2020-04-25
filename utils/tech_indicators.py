import pandas_datareader.data as web
import matplotlib.pyplot as plt
import datetime


def MACD(DF, a, b, c):
    df = DF.copy()
    df["MA_Fast"] = df["Adj Close"].ewm(span = a, min_periods = a).mean()
    df["MA_Slow"] = df["Adj Close"].ewm(span = b, min_periods = b).mean()
    df["MACD"] = df["MA_Fast"] - df["MA_Slow"]
    df["Signal"] = df["MACD"].ewm(span = c, min_periods = c).mean()
    df.dropna(inplace = True)
    return df


def Bollinger_Bands(DF, n):
    """
    this function calculates the bollinger bands
    """
    df = DF.copy()
    df["MA"] = df['Adj Close'].rolling(n).mean()
    df["BB_up"] = df["MA"] + 2*df['Adj Close'].rolling(n).std(ddof=0)
    df["BB_dn"] = df["MA"] - 2*df['Adj Close'].rolling(n).std(ddof=0)
    df["BB_width"] = df["BB_up"] - df["BB_dn"]
    df.dropna(inplace=True)
    return df


def ATR(DF, n):
    """
    Calculates ATR for the given period
    """
    df = DF.copy()
    df['H-L'] = abs(df['High'] - df['Low'])
    df['H-PC'] = abs(df['High'] - df['Adj Close'].shift(1))
    df['L-PC'] = abs(df['Low'] - df['Adj Close'].shift(1))
    df['TR']=df[['H-L','H-PC','L-PC']].max(axis=1,skipna=False)
    df['ATR'] = df['TR'].rolling(n).mean()
    #df['ATR'] = df['TR'].ewm(span=n,adjust=False,min_periods=n).mean()
    df2 = df.drop(['H-L','H-PC','L-PC'],axis=1)
    return df2