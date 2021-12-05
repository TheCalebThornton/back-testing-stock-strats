from fastquant import backtest
from fbprophet import Prophet

def smac (dataSet, initCash=10000, plot=False, verbose=False):
    backtest('smac',
       dataSet,
       init_cash=initCash,
       fast_period=[7,14,21,28],
       slow_period=[30,45,60,75],
       plot=False,
       verbose=False
      )

def rsi (dataSet, initCash=10000, plot=False, verbose=False):
     backtest('rsi',
         dataSet,
         init_cash=initCash,
         rsi_upper=[75, 65],
         rsi_lower=[40, 35],
         rsi_period=[10,14],
         plot=False,
         verbose=False
        )

def buyAndHold (dataSet, initCash=10000, plot=False, verbose=False):
    backtest('buynhold',
       dataSet,
       init_cash=initCash,
       plot=False,
       verbose=False
    )

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

# stock_data["custom"] = stock_data.close.pct_change()
# custom_res, history = backtest('custom',
#                  stock_data,
#                  init_cash=cashToTrade,
#                  upper_limit=[0.05, 0.07, 0.5],
#                  lower_limit=[0.03, 0.01, 0.005],
#                  plot=False,
#                  verbose=False,
#                  return_history=True
#                 )
