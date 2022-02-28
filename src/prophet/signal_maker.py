from fastquant import get_stock_data, get_crypto_data, backtest
import sys
import os
from datetime import date
# Python imports are super annoying - modify this path with your own
sys.path.append(os.path.abspath("/Users/cthornton/devl/workspace/back-testing-stock-strats"))
from src.prophet.strategies import give_me_next_signal

# ticker = "BTC/USDT"
# cashToTrade = 10000
# stock_data = get_crypto_data(ticker,
#                          "2020-12-09",
#                          "2021-12-09",
#                          time_resolution='1d'
#                         )
today = date.today().strftime("%Y-%m-%d")
print("Today's date:", today)

OPTIMAL_UPPER = 2.0
OPTIMAL_LOWER = -2.0
ticker = "BTC/USDT"
stock_data = get_crypto_data(ticker,
                            "2019-12-09",
                            today)

give_me_next_signal(stock_data, optimal_lower=OPTIMAL_LOWER, optimal_upper=OPTIMAL_UPPER)
