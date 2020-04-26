from utils import data_call as dc
from utils import tech_indicators as ti
import pandas as pd


TICKERS = ["IBM", "AAPL", "TSLA", "NVDA"]
atr_periods = [3, 7, 55]

# Yahoo API
generated_data_daily = dc.generate_data(TICKERS, interval="d", n_per=90)

data_with_atr = {}
for k,v in generated_data_daily.items():
    v_ = v.copy()
    for i in atr_periods:
        v_[f"ATR_{i}"] = ti.ATR(v_, i)
    data_with_atr.update({k:v_})
    

# # test for slow_fast_SMA function
# import pandas as pd
# import matplotlib.pyplot as plt
# plt.style.use("ggplot")
#
# kk = pd.read_csv("data/data_AAPL.csv")
# kk = slow_fast_SMA(kk, 100, 200)
# kk[["Adj Close", "sma_fast", "sma_slow"]].plot()
# plt.show()
# # test for stochastic function
# import pandas as pd
# import matplotlib.pyplot as plt
# plt.style.use("ggplot")
#
# kk = pd.read_csv("data/data_AAPL.csv")
# kk = slow_fast_SMA(kk, 100, 200)
# kk = stochastic(kk, 14, 3, 3)
# kk[["Adj Close", "sma_fast", "sma_slow"]].plot()
# plt.figure(figsize=(20, 8))
# kk[["k", "D"]].plot(alpha = 0.5)
# plt.show()
