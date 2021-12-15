from fastquant import get_stock_data, backtest
from src.utils.strategies import *

ticker = "TQQQ"
cashToTrade = 10000
stock_data = get_stock_data(ticker,
                            "2010-12-02",
                            "2021-12-04")

print (stock_data)
#
# # the result set should come back pre-sorted, so i'm grabbing the top one.
# smac_res = smac(stock_data).iloc[0]
# smac_res.cust_name='SMAC'
# rsi_res = rsi(stock_data).iloc[0]
# rsi_res.cust_name='RSI'
# bnh_res = buy_and_hold(stock_data).iloc[0]
# bnh_res.cust_name='BuyNHold'
#
# print (f'INVESTMENT STRAT RESULTS - {ticker}')
# print_sorted_results([smac_res,
#                     rsi_res,
#                     bnh_res])


stochastic_smac_hybrid(stock_data)
