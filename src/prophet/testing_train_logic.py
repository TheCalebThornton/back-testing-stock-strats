from fastquant import get_stock_data, get_crypto_data, backtest
import sys
import os
# Python imports are super annoying - modify this path with your own
sys.path.append(os.path.abspath("/Users/cthornton/devl/workspace/back-testing-stock-strats"))
from src.prophet.strategies import *
from src.utils.strategies import smac, rsi, buy_and_hold, print_sorted_results

ticker = "ETH/USDT"
stock_data = get_crypto_data(ticker,
                            "2021-12-01",
                            "2021-12-10",
                            time_resolution='1d')
prophet(stock_data)
