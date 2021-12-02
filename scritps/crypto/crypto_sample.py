from fastquant import get_crypto_data
from fastquant import backtest

def print_best_results_and_config(results):
    # get best parameters on top row
    top_result = results.iloc[0]
    init_cash = getattr(top_result, 'init_cash', None)
    final_value = getattr(top_result, 'final_value', None)
    fast_best = getattr(top_result, 'fast_period', None)
    slow_best = getattr(top_result, 'slow_period', None)
    prcntGain = (final_value / init_cash - 1) * 100
    print ('BEST RESULTS:')
    print (f'initial_cash: {init_cash}. final_cash: {final_value}. Percentage Gain: {prcntGain}')
    print ('BEST CONFIGURATION PARAMS:')
    print (f'fast_period: {fast_best}. slow_period: {slow_best} final_value: {final_value}')

crypto = get_crypto_data("ETH/USDT",
                         "2018-12-01",
                         "2021-12-01",
                         time_resolution='1d'
                        )
print ('LAST 5 DAYS OF CRYPTO DATA')
# print (crypto.tail())

smac_res = backtest('smac',
                   crypto,
                   fast_period=[7,14,21,28],
                   slow_period=[30,45,60,75],
                   plot=False,
                   verbose=False
                  )

bnh_res = backtest('buynhold',
                   crypto,
                   plot=False,
                   verbose=False
                  )
print ('INVESTMENT STRAT RESULTS')
print ('Buy And Hold')
print_best_results_and_config(bnh_res)
print ('SMAC')
print_best_results_and_config(smac_res)




# run backtest using optimum values
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
