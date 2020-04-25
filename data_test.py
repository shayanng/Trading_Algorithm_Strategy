from utils import data_call as dc
from utils import tech_indicators as ti
import pandas as pd

ASSET = "IBM"
df = pd.read_csv(f"./data/data_{ASSET}.csv") # read data
atr_periods = [3, 7, 55]

for i in atr_periods:
    df[f"ATR_{i}"] = ti.ATR(df, i)

print(df)