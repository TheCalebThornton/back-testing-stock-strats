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
ticker = "ETH/USDT"
stock_data = get_crypto_data(ticker,
                            "2020-12-10",
                            "2021-12-10",
                            time_resolution='1d')
# CAREFUL WITH THIS. Prophet will attempt to predict weekends... The NYSE stock market is closed on weekends/holidays
# TODO: Update Prophet algo to accomodate holidays and weekends for NYSE market
# ticker = "TQQQ"
# stock_data = get_stock_data(ticker,
#                             "2018-12-09",
#                             "2021-12-09")
print (stock_data)

# the result set should come back pre-sorted, so i'm grabbing the top one.
smac_res = smac(stock_data).iloc[0]
smac_res.cust_name='SMAC'
rsi_res = rsi(stock_data).iloc[0]
rsi_res.cust_name='RSI'
bnh_res = buy_and_hold(stock_data).iloc[0]
bnh_res.cust_name='BuyNHold'
proph_res = prophet(train_data, stock_data).iloc[0]
proph_res.cust_name='Prophet'

print (f'INVESTMENT STRAT RESULTS - {ticker}')
print_sorted_results([smac_res,
                    rsi_res,
                    bnh_res,
                    proph_res])
