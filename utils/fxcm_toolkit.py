

def create_ohlc(fxcm_df):
    fxcm_df["open"] = (fxcm_df["bidopen"] + fxcm_df["askopen"])/2
    fxcm_df["high"] = (fxcm_df["bidhigh"] + fxcm_df["askhigh"])/2
    fxcm_df["low"] = (fxcm_df["bidlow"] + fxcm_df["asklow"])/2
    fxcm_df["close"] = (fxcm_df["bidclose"] + fxcm_df["askclose"])/2
    # fxcm_df(["bidopen", "askopen", "bidhigh", "askhigh", "bidlow", "asklow",
    #          "bidclose", "askclose", "tickqty"]).drop(inplace=True)
    return fxcm_df[["open", "high", "low", "close"]]