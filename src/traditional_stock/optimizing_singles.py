from fastquant import get_stock_data, get_crypto_data, backtest
from src.utils.strategies import *

ticker = "ETH/USDT"
cashToTrade = 10000
# stock_data = get_stock_data(ticker,
#                             "2019-01-01",
#                             "2019-12-18")
stock_data = get_crypto_data(ticker,
                         "2019-01-01",
                         "2021-12-18",
                         time_resolution='1d'
                        )

print (stock_data)

stoch_optimal = optimize_stochastic_smac_hybrid_results(stock_data)
try:
    stoch_optimal.sort(key=lambda x: x.win_rate, reverse=True)
except:
    print("Not an Array, can't sort")
# Top 5 results
# print(f'Optimal: {stoch_optimal[:2]}')
print_sorted_results(stoch_optimal[:7])
