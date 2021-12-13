from fastquant import get_stock_data, get_crypto_data, backtest
import sys
import os
# Python imports are super annoying - modify this path with your own
sys.path.append(os.path.abspath("/Users/cthornton/devl/workspace/back-testing-stock-strats"))
from src.prophet.strategies import prophet
from src.utils.strategies import smac, rsi, buy_and_hold, print_sorted_results

# ticker = "BTC/USDT"
# cashToTrade = 10000
# stock_data = get_crypto_data(ticker,
#                          "2020-12-09",
#                          "2021-12-09",
#                          time_resolution='1d'
#                         )
ticker = "TQQQ"
stock_data = get_stock_data(ticker,
                            "2018-12-09",
                            "2021-12-09")

give_me_a_signal(stock_data)
