from fastquant import get_stock_data, get_crypto_data, backtest
from src.utils.strategies import *

# ticker = "ETH/USDT"
ticker = "TQQQ"
cashToTrade = 10000
stock_data_1 = get_stock_data(ticker,
                            "2019-01-01",
                            "2020-01-01")
stock_data_2 = get_stock_data(ticker,
                            "2020-01-01",
                            "2021-01-01")
stock_data_3 = get_stock_data(ticker,
                            "2021-01-01",
                            "2022-01-01")
stock_data_4 = get_stock_data(ticker,
                            "2018-01-01",
                            "2019-01-01")
stock_data_5 = get_stock_data(ticker,
                            "2018-01-01",
                            "2022-01-01")
stock_data_6 = get_stock_data(ticker,
                            "2021-12-01",
                            "2022-03-22")
# stock_data_1 = get_crypto_data(ticker,
#                          "2019-01-01",
#                          "2021-12-18",
#                          time_resolution='1d'
#                         )


# print (stock_data)

stoch_optimal = optimize_stochastic_smac_hybrid_results([stock_data_1, stock_data_2, stock_data_3, stock_data_4, stock_data_5, stock_data_6])
# Top 5 results
print('SUCCESS, see csv output')
# print(f'Optimal: {stoch_optimal[:5]}')
# print_sorted_results(stoch_optimal[:7])
