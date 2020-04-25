from utils import data_call as dc
from utils import tech_indicators as ti
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import numpy as np
import pandas_datareader.data as web
import pandas as pd
import datetime
import time
import sys
import statsmodels.api as sm
plt.style.use("ggplot")

TICKERS = ["IBM", "AAPL", "TSLA", "NVDA"]

generated_data_daily = dc.generate_data(TICKERS, interval="d", n_per=90)

daily_ATR3_IBM = ti.ATR(generated_data_daily["IBM"], 3)
daily_ATR7_IBM = ti.ATR(generated_data_daily["IBM"], 7)
daily_ATR55_IBM = ti.ATR(generated_data_daily["IBM"], 55)