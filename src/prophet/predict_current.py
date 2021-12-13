import sys
import os
# Python imports are super annoying - modify this path with your own
sys.path.append(os.path.abspath("/Users/cthornton/devl/workspace/back-testing-stock-strats"))
from fastquant import get_stock_data, get_crypto_data, backtest
from src.prophet.strategies import *
from datetime import date

today = date.today().strftime("%Y-%m-%d")
print("Today's date:", today)

OPTIMAL_UPPER = 2.0
OPTIMAL_LOWER = -2.0

ticker = "BTC/USDT"
stock_data = get_crypto_data(ticker,
                            "2016-12-09",
                            today,
                            time_resolution='1d')

print (stock_data)
give_me_next_signal(stock_data, OPTIMAL_UPPER, OPTIMAL_LOWER)
