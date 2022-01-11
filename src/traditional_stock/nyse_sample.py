from fastquant import get_stock_data, backtest
from src.utils.strategies import *

ticker = "TQQQ"
cashToTrade = 10000
stock_data = get_stock_data(ticker,
                            "2021-01-01",
                            "2021-12-30")
print (stock_data)

# the result set should come back pre-sorted, so i'm grabbing the top one.
smac_res = smac(stock_data).iloc[0]
smac_res.cust_name='SMAC'
rsi_res = rsi(stock_data).iloc[0]
rsi_res.cust_name='RSI'
bnh_res = buy_and_hold(stock_data).iloc[0]
bnh_res.cust_name='BuyNHold'
stoch_hybrid_res = stochastic_smac_hybrid(stock_data, stratOptions={'length': 1, 'smoothK': 1, 'smoothD': 5, 'upperBound': 64, 'lowerBound': 20}).iloc[0]
stoch_hybrid_res.cust_name='Stochastic Smac Hybrid'

print_sorted_results([stoch_hybrid_res, bnh_res, smac_res, rsi_res])
