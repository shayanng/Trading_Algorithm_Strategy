import pandas as pd
import  time
import datetime as dt
from utils import data_call as dc
from utils import tech_indicators as ti
from utils import fxcm_toolkit as fxtlk
from utils import preprocessing
from utils import trading
from utils import visuals

# FXCM Demo Account!
DEMO_FXCM_R = "7d98094ee68f29fb83fd276bcb611556e55769f5"
TICKERS = ["EUR/USD", "GBP/USD","USD/CAD"]
PERIOD = "D1"
START = dt.datetime(2015, 1, 1)
END = dt.datetime(2019, 1, 1)
data_fxcm_dict = fxtlk.get_fxcm_data(token=DEMO_FXCM_R, tickers=TICKERS, period=PERIOD, start=START, end=END) # call api

#average bid/ask (consider OHLC only)
data_fxcm_ohlc = {}
for ticker, fxcmdf in data_fxcm_dict.items():
    ohlc = fxtlk.create_ohlc(fxcmdf)
    data_fxcm_ohlc.update({ticker:ohlc})

# apply strategy and plot
df = data_fxcm_ohlc["GBP/USD"]
df_signals = trading.apply_sma_co(dataframe=df, on="Close", period=50) # apply strategy

# other indicators jsut for visualisation purposes. (actual strategy is on 50 moving average)
df["sma_100"] = ti.getSMA(df, 100, "Close")
df["sma_200"] = ti.getSMA(df, 200, "Close")
df["sma_300"] = ti.getSMA(df, 300, "Close")

sma_plot = visuals.plot_trades(df_signals, on="Close", indicators=["sma", "sma_100", "sma_200", "sma_300"]) # plot trades
sma_plot.show()

# # Stochastic Test
# kk = pd.read_csv("data/data_AAPL.csv")
# kk = slow_fast_SMA(kk, 100, 200)
# kk = stochastic(kk, 14, 3, 3)
# kk[["Adj Close", "sma_fast", "sma_slow"]].plot()
# plt.figure(figsize=(20, 8))
# kk[["k", "D"]].plot(alpha = 0.5)
# plt.show()
