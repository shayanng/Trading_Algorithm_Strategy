import plotly.graph_objects as go

def plot_trades(signals_df, on, indicators:list, template="plotly_dark"):
    """
    Plots financial timeseries data along with buy/sell signals generated by trading algorith.

    Args:
        signals_df: dataframe containing 'signal' column.
        on: string - e.g: Close, Open, Adj Close, etc... Must match what was used in trading strategy.
        indicators: list - name of the column of required indicators. e.g: if you want to plot 
                     simple moving average, give the name of the column containing the sma.
        template: string - default="plotly_dark" : plotly template 

    Returns:
        fig - plotting figure
    """

    # Separate buy and sell data points
    df_buys = signals_df[signals_df["signal"]=="BUY"]
    df_sells = signals_df[signals_df["signal"]=="SELL"]
    # df_rest = signals_df[signals_df["signal"]=="NO_ACTION"]


    fig = go.Figure()

    # Actual market movement
    fig.add_trace(go.Scatter(
        x=signals_df.index,
        y=signals_df[on],
        name=on,
    #     mode='lines',
    #     line_color='#257EDC',
    #     opacity=0.8
        )
    )

    # plot indicators
    for i in indicators:
        fig.add_trace(go.Scatter(
            x=signals_df.index,
            y=signals_df[i],
            name=i.upper(),
            # line_color='#c761ff',
            line=dict(width=2, dash="dot"),
            opacity=0.8
            )
        )

    # BUY signals
    fig.add_trace(go.Scatter(
        x=df_buys.index,
        y=df_buys[on],
        name="BUY",
        mode='markers',
        opacity=1,
        marker_symbol="triangle-up",
        marker=dict(
            color='#39ff14',
            size=10
            )
        )
    )

    # SELL signals
    fig.add_trace(go.Scatter(
        x=df_sells.index,
        y=df_sells[on],
        name="SELL",
        mode='markers',
        opacity=1,
        marker_symbol="triangle-down",
        marker=dict(
            color='#ff0800',
            size=10
            )
        )
    )

    fig.update_layout(
        title=f'Trading Chart',
        xaxis_title='Date',
        yaxis_title='Price',
        template=template,
    )


    return fig