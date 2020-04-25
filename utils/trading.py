def apply_sma_co(dataframe, on):
    """
    Applies SMA crossover strategy

    Args:
        dataframe: pandas dataframe.
        on: requested column (e.g: Adj close, close, etc)


    Returns:
        dataframe containing the signal
    """
    def get_signal(x):
        if ((x["shifted_value"] < x["shifted_sma"]) and (x[on] > x["sma"])):
            return("BUY")
        elif ((x["shifted_value"] > x["shifted_sma"]) and (x[on] < x["sma"])):
            return("SELL")
        else:
            return("NO_ACTION")
    dataframe["signal"] = dataframe.apply(get_signal, axis=1)
    return dataframe