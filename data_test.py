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
    
print(data_with_atr)
print("hi")
#%%


