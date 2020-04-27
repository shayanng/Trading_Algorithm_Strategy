from utils import fxcm_toolkit as ft
from utils import data_call as dc
from utils import tech_indicators as ti
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import numpy as np
import pandas_datareader.data as web
import pandas as pd
import fxcmpy
import socketio.client
import socketIO_client
import datetime
import time
import sys
import statsmodels.api as sm
plt.style.use("ggplot")


token = "0410b9efc56ba9202e68ccab7286bd6b2d2dc9d0"
con = fxcmpy.fxcmpy(access_token=token, log_level="error", server = "demo", log_file="log.txt")


pair = "EUR/USD"

# start = datetime.datetime(2015, 1, 3)
# stop = datetime.datetime(2018, 3, 1)
# df = con.get_candles("EUR/USD", period="D1", start=start, end=stop)

eur_usd_m5 = con.get_candles(pair, period = 'm5', number = 3250)
eur_usd_m15 = con.get_candles(pair, period = 'm15', number = 3250)
eur_usd_h1 = con.get_candles(pair, period = 'H1', number = 3250)
eur_usd_d1 = con.get_candles(pair, period = 'D1', number = 3250)

eur_usd_m5 = ft.create_ohlc(eur_usd_m5)
eur_usd_m15 = ft.create_ohlc(eur_usd_m15)
eur_usd_h1 = ft.create_ohlc(eur_usd_h1)
eur_usd_d1 = ft.create_ohlc(eur_usd_d1)


#test for data generated
# eur_usd_d1[["open", "close"]].plot(alpha=0.6)
# plt.show()
def ATR(DF, n):
    """
    Calculates ATR for the given period
    """
    df = DF.copy()
    df['H-L'] = abs(df['High'] - df['Low'])
    df['H-PC'] = abs(df['High'] - df['Close'].shift(1))
    df['L-PC'] = abs(df['Low'] - df['Close'].shift(1))
    df['TR']=df[['H-L','H-PC','L-PC']].max(axis=1,skipna=False)
    df['ATR'] = df['TR'].rolling(n).mean()
    #df['ATR'] = df['TR'].ewm(span=n,adjust=False,min_periods=n).mean()
    df2 = df.drop(['H-L','H-PC','L-PC'],axis=1)
    return df2

# eur_usd_atr05_m5 = ATR(eur_usd_m5, 3)
# eur_usd_atr07_m5 = ATR(eur_usd_m5, 7)
# eur_usd_atr55_m5 = ATR(eur_usd_m5, 55)
#
# eur_usd_atr05_h1 = ATR(eur_usd_h1, 3)
# eur_usd_atr07_h1 = ATR(eur_usd_h1, 7)
# eur_usd_atr55_h1 = ATR(eur_usd_h1, 55)
#
# eur_usd_atr05_d1 = ti.ATR(eur_usd_d1, 3)
# eur_usd_atr07_d1 = ti.ATR(eur_usd_d1, 7)
# eur_usd_atr55_d1 = ti.ATR(eur_usd_d1, 55)


def ATR_dataframe(DF, per1, per2, per3):
    df = DF.copy()
    df[f"ATR{per1}"] = ATR(df, per1)
    df[f"ATR{per2}"] = ATR(df, per2)
    df[f"ATR{per3}"] = ATR(df, per3)
    return df

#calling for the ATR_dataframe function
eur_usd_atr_h1 = ATR_dataframe(eur_usd_h1, 5, 7, 55)