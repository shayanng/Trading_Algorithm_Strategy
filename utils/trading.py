from utils import tech_indicators as ti
from utils import preprocessing

def apply_sma_co(dataframe, on, period):

    # get moving average
    dataframe["sma"] = ti.getSMA(dataframe=dataframe, period=period, on=on)

    # process data
    df = preprocessing.getPervValues(dataframe=dataframe, period=1, on=on) # Period MUST be 1 here.

    """
    Applies SMA crossover strategy.

    Args:
        dataframe: collected data.
        on: requested column (e.g: Adj close, close, etc).
        period: the window of moving average.


    Returns:
        dataframe containing the signal.
    """
    def get_signal(x):
        if ((x["shifted_value"] < x["shifted_sma"]) and (x[on] > x["sma"])):
            return("BUY")
        elif ((x["shifted_value"] > x["shifted_sma"]) and (x[on] < x["sma"])):
            return("SELL")
        else:
            return("NO_ACTION")
    df["signal"] = df.apply(get_signal, axis=1) # perform the logic of the trade
    return df