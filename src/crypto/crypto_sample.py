from fastquant import get_crypto_data, backtest
from src.utils.strategies import *

ticker = "ETH/USDT"
cashToTrade = 10000
stock_data = get_crypto_data(ticker,
                         "2021-12-01",
                         "2022-03-07",
                         time_resolution='1d'
                        )

print (stock_data)

# the result set should come back pre-sorted, so i'm grabbing the top one.
smac_res = smac(stock_data).iloc[0]
smac_res.cust_name='SMAC'
# rsi_res = rsi(stock_data).iloc[0]
# rsi_res.cust_name='RSI'
bnh_res = buy_and_hold(stock_data).iloc[0]
bnh_res.cust_name='BuyNHold'
stoch_hybrid_res, stoch_hybrid_hist  = stochastic_smac_hybrid(stock_data, stratOptions={'length': 3, 'smoothK': 3, 'smoothD': 5, 'upperBound': 80, 'lowerBound': 45})
stoch_hybrid_res = stoch_hybrid_res.iloc[0]
stoch_hybrid_res.cust_name='Stochastic Smac Hybrid'

print_sorted_results([smac_res,
                    # rsi_res,
                    bnh_res,
                    stoch_hybrid_res])
