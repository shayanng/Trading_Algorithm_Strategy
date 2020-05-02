import oandapyV20
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.orders as orders
import matplotlib.pyplot as plt
import pandas as pd
plt.style.use("ggplot")


API_path = "C:\\Users\\naghi\\API keys\\Oanda_API.txt"
client = oandapyV20.API(access_token=open(API_path, "r").read(),
                        environment="practice")


account_id = "101-002-8118126-012"


#tools for oanda data manupulations and order
def candles(instrument, n_candles: int = 250, timeframe: str = "H1"):
    """
    function to get data from Oanda API
    """
    params = {"count": n_candles, "granularity": timeframe}
    candles = instruments.InstrumentsCandles(instrument=instrument, params=params)
    client.request(candles)
    ohlc_dict = candles.response["candles"]
    ohlc = pd.DataFrame(ohlc_dict)
    ohlc_df = ohlc.mid.dropna().apply(pd.Series)
    ohlc_df["volume"] = ohlc["volume"]
    ohlc_df.index = ohlc["time"]
    ohlc_df = ohlc_df.apply(pd.to_numeric)
    return ohlc_df


def market_order(instrument, units, sl):
    """
    units can be positive or negative, stop loss (in pips) added/subtracted to price
    """
    account_ID = account_id
    data = {
            "order": {
            "price": "",
            "stopLossOnFill": {
            "trailingStopLossOnFill": "GTC",
            "distance": str(sl)
                              },
            "timeInForce": "FOK",
            "instrument": str(instrument),
            "units": str(units),
            "type": "MARKET",
            "positionFill": "DEFAULT"
                    }
            }
    r = orders.OrderCreate(accountID=account_ID, data=data)
    client.request(r)


def trade_signal(df, curr):
    """
    Generates signal
    """
    global upward_sma_dict, downward_sma_dict
    signal = ""
    if df["sma_fast"][-1] > df["sma_slow"] and df["sma_fast"][-2] < df["sma_slow"][-2]:
        upward_sma_dict[curr] = True
        downward_sma_dict[curr] = False
    if df["sma_fast"][-1] < df["sma_slow"] and df["sma_fast"][-2] > df["sma_slow"][-2]:
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


def ATR(DF,n):
    "function to calculate True Range and Average True Range"
    df = DF.copy()
    df['H-L']=abs(df['h']-df['l'])
    df['H-PC']=abs(df['h']-df['c'].shift(1))
    df['L-PC']=abs(df['l']-df['c'].shift(1))
    df['TR']=df[['H-L','H-PC','L-PC']].max(axis=1,skipna=False)
    df['ATR'] = df['TR'].rolling(n).mean()
    #df['ATR'] = df['TR'].ewm(span=n,adjust=False,min_periods=n).mean()
    df2 = df.drop(['H-L','H-PC','L-PC'],axis=1)
    return round(df2["ATR"][-1],2)