def getPervValues(dataframe, period, on):
    """
    Gets previous values of sma and requested column.

    Args:
        dataframe: pandas dataframe.
        period: the value on this many indecies in the past.
        on: requested column (e.g: Adj close, close, etc)


    Returns:
        dataframe containing the shifted values of sma and the requested column
    """
    dataframe["shifted_value"] = dataframe[on].shift(period)
    dataframe["shifted_sma"] = dataframe["sma"].shift(period)
    
    return dataframe
