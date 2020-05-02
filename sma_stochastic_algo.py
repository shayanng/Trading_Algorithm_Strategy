import oandapyV20
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
from utils import oanda_toolkit as oanda
from utils import tech_indicators as tech
from utils import visuals as visual
import pandas as pd
import matplotlib.pyplot as plt
import time

# Connecting to API
API_path = "C:\\Users\\naghi\\API keys\\Oanda_API.txt"
client = oandapyV20.API(access_token=open(API_path, "r").read(),
                        environment="practice")

account_id = "101-002-8118126-012"

# pairs for EU & US sessions
pairs = ['EUR_USD','GBP_USD','USD_CHF','USD_CAD']

pos_size = 2000
upward_sma_dict = {}
downward_sma_dict = {}
for i in pairs:
    upward_sma_dict[i] = False
    downward_sma_dict[i] = False

# instrument = "EUR_USD"
# n_candles = 250
# timeframe = "H1"

# r = accounts.AccountDetails(account_id)
# client.request(r)
# print(r.response)

def trade_signal(df, curr):
    """
    Generates signal
    """
    global upward_sma_dict, downward_sma_dict
    signal = ""
    if df["sma_fast"][-1] > df["sma_slow"][-1] and df["sma_fast"][-2] < df["sma_slow"][-2]:
        upward_sma_dict[curr] = True
        downward_sma_dict[curr] = False
    if df["sma_fast"][-1] < df["sma_slow"][-1] and df["sma_fast"][-2] > df["sma_slow"][-2]:
        upward_sma_dict[curr] = False
        downward_sma_dict[curr] = True
    if upward_sma_dict[curr] == True and min(df["K"][-1], df["D"][-1]) > 25 and max((df["K"][-2], df["D"][-2])) < 25:
        signal = "Buy"
    if downward_sma_dict[curr] == True and min(df["K"][-1], df["D"][-1]) > 75 and max((df["K"][-2], df["D"][-2])) < 75:
        signal = "Sell"

    plt.subplot(211)
    plt.plot(df.loc[:, ['c', 'sma_fast', 'sma_slow']])
    plt.title('SMA Crossover & Stochastic')
    plt.legend(('close', 'sma_fast', 'sma_slow'), loc='upper left')

    plt.subplot(212)
    plt.plot(df.loc[:, ['K', 'D']])
    plt.hlines(y=25, xmin=0, xmax=len(df), linestyles='dashed')
    plt.hlines(y=75, xmin=0, xmax=len(df), linestyles='dashed')
    plt.show()
    return signal

# backtest
for currency in pairs:
    print("processing:", currency)
    data = oanda.candles(currency, n_candles=500, timeframe="H1")
    ohlc_df = tech.stochastic(data, 14, 3, 3)
    ohlc_df = tech.SMA_slow_fast(ohlc_df, 100, 200)
    signal = trade_signal(ohlc_df, currency)
