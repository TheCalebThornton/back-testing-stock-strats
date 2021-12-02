from fastquant import get_crypto_data
from fastquant import backtest

crypto = get_crypto_data("ETH/USDT",
                         "2018-12-01",
                         "2019-12-31",
                         time_resolution='1d'
                        )
print (crypto.tail())

results = backtest('smac',
                   crypto,
                   fast_period=[7,14,21,28],
                   slow_period=[30,45,60,75],
                   plot=False,
                   verbose=False
                  )
results.head()
print ('I ran line 19')

#get best parameters on top row
# fast_best, slow_best = results.iloc[0][["fast_period","slow_period"]]
# fast_best, slow_best
# import matplotlib as pl
# pl.style.use("default")
# pl.rcParams["figure.figsize"] = (9,5)
# results = backtest('smac',
#                    crypto,
#                    fast_period=fast_best,
#                    slow_period=slow_best,
#                    plot=True,
#                    verbose=False
#                   )
