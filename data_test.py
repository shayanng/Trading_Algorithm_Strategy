from utils import data_call as dc
from utils import tech_indicators as ti
from utils import fxcm_toolkit as fxtlk
import pandas as pd
import  time
import fxcmpy
import socketio
import socketIO_client
import datetime as dt
# import matplotlib.pyplot as plt
# plt.style.use("ggplot")


# FXCM Demo Account!
DEMO_FXCM_R = "7d98094ee68f29fb83fd276bcb611556e55769f5"
TICKERS = ["EUR/USD", "GBP/USD","USD/CAD"]
PERIOD = "m15"
START = dt.datetime(2018, 1, 1)
END = dt.datetime(2018, 3, 1)
data_fxcm_dict = fxtlk.get_fxcm_data(token=DEMO_FXCM_R, tickers=TICKERS, period=PERIOD, start=START, end=END) # call api

# average bid/ask (consider OHLC only)
data_fxcm_ohlc = {}
for ticker, fxcmdf in data_fxcm_dict.items():
    ohlc = fxtlk.create_ohlc(fxcmdf)
    data_fxcm_ohlc.update({ticker:ohlc})
    
print(data_fxcm_ohlc)

# Yahoo API
# TICKERS = ["IBM", "AAPL", "TSLA", "NVDA"]
# generated_data_daily = dc.generate_data(TICKERS, interval="d", n_per=90)

# ATR Test
# atr_periods = [3, 7, 55]
# data_with_atr = {}
# for k,v in generated_data_daily.items():
#     v_ = v.copy()
#     for i in atr_periods:
#         v_[f"ATR_{i}"] = ti.ATR(v_, i)
#     data_with_atr.update({k:v_})

# # Stochastic Test
# kk = pd.read_csv("data/data_AAPL.csv")
# kk = slow_fast_SMA(kk, 100, 200)
# kk = stochastic(kk, 14, 3, 3)
# kk[["Adj Close", "sma_fast", "sma_slow"]].plot()
# plt.figure(figsize=(20, 8))
# kk[["k", "D"]].plot(alpha = 0.5)
# plt.show()
