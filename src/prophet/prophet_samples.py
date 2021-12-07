from fastquant import backtest
from prophet import Prophet

# FaceBook Prophet impl
def prophet ():
    # Fit model on closing prices
    ts = df.reset_index()[["dt", "close"]]
    ts.columns = ['ds', 'y']
    m = Prophet(daily_seasonality=True, yearly_seasonality=True).fit(ts)
    forecast = m.make_future_dataframe(periods=0, freq='D')

    # Predict and plot
    pred = m.predict(forecast)
    fig1 = m.plot(pred)
    plt.title('BTC/USDT: Forecasted Daily Closing Price', fontsize=25)
