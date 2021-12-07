from fastquant import get_crypto_data, backtest
from src.utils.strategies import smac, rsi, buy_and_hold, print_sorted_results

ticker = "ETH/USDT"
cashToTrade = 10000
stock_data = get_crypto_data(ticker,
                         "2018-12-01",
                         "2021-12-01",
                         time_resolution='1d'
                        )

print (stock_data)

# the result set should come back pre-sorted, so i'm grabbing the top one.
smac_res = smac(stock_data).iloc[0]
smac_res.cust_name='SMAC'
rsi_res = rsi(stock_data).iloc[0]
rsi_res.cust_name='RSI'
bnh_res = buy_and_hold(stock_data).iloc[0]
bnh_res.cust_name='BuyNHold'

print (f'INVESTMENT STRAT RESULTS - {ticker}')
print_sorted_results([smac_res,
                    rsi_res,
                    bnh_res])
