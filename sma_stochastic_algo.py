import oandapyV20
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
import pandas as pd
import matplotlib.pyplot as plt
import time


# pairs for EU & US sessions
pairs = ['EUR_USD','GBP_USD','USD_CHF','USD_CAD']

pos_size = 2000
upward_sma_dict = {}
downward_sma_dict = {}
for i in pairs:
    upward_sma_dict[i] = False
    downward_sma_dict[i] = False