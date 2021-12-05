from fastquant import get_stock_data, backtest
from ../strategies.py import smac, rsi, buyAndHold, prophet

def print_best_results_and_config(results):
    # get best parameters on top row
    top_result = results.iloc[0]
    init_cash = getattr(top_result, 'init_cash', None)
    final_value = getattr(top_result, 'final_value', None)
    param1 = getattr(top_result, 'fast_period', getattr(top_result, 'rsi_upper', getattr(top_result, 'upper_limit', None)))
    param2 = getattr(top_result, 'slow_period', getattr(top_result, 'rsi_lower', getattr(top_result, 'lower_limit', None)))
    param3 = getattr(top_result, 'rsi_period', None)
    prcntGain = (final_value / init_cash - 1) * 100
    print ('BEST RESULTS:')
    print (f'initial_cash: {init_cash}. final_cash: {final_value}. Percentage Gain: {prcntGain}')
    print ('BEST CONFIGURATION PARAMS:')
    print (f'param1: {param1}. param2: {param2}. param3: {param3}')

ticker = "TQQQ"
cashToTrade = 10000
stock_data = get_stock_data(ticker,
                            "2020-12-02",
                            "2021-12-04")

print (stock_data)

smac_res = backtest('smac',
                   stock_data,
                   init_cash=cashToTrade,
                   fast_period=[7,14,21,28],
                   slow_period=[30,45,60,75],
                   plot=False,
                   verbose=False
                  )

rsi_res = backtest('rsi',
                 stock_data,
                 init_cash=cashToTrade,
                 rsi_upper=[75, 65],
                 rsi_lower=[40, 35],
                 rsi_period=[10,14],
                 plot=False,
                 verbose=False
                )

# FaceBook Prophet impl
# Pull crypto data
df = get_crypto_data("BTC/USDT", "2019-01-01", "2020-05-31")

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

bnh_res = backtest('buynhold',
                   stock_data,
                   init_cash=cashToTrade,
                   plot=False,
                   verbose=False
                  )
print (f'INVESTMENT STRAT RESULTS - {ticker}')
print ('Buy And Hold')
print_best_results_and_config(bnh_res)
print ('SMAC')
print_best_results_and_config(smac_res)
print ('RSI')
print_best_results_and_config(rsi_res)
print ('CUSTOM')
print_best_results_and_config(custom_res)
