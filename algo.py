import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from utils import data_call as dc
from utils import tech_indicators as ti
from utils import preprocessing
from utils import trading

TICKERS = ["IBM", "AAPL", "TSLA", "NVDA"]
AV_KEY = "3R9JOE98DJOXYHKJ" # alpha-vantage demo api
ts = TimeSeries(key=AV_KEY, output_format="pandas")  # initialise timeseries av

# Yahoo API
# generated_data_daily = dc.generate_data(TICKERS, interval="d", n_per=90)

# AlphaVantage API
# generated_data = dc.generate_data_intraday(tickers=TICKERS, interval="5min", outputsize="full",
#                                ts=ts)  # dictionary of collected data

# for k in generated_data.keys():
#     generated_data[k].to_csv(f"./data/data_{k}.csv")  # save as csv




