from fastquant import get_stock_data, backtest
from src.utils.strategies import *

ticker = "TQQQ"
cashToTrade = 10000
stock_data = get_stock_data(ticker,
                            "2017-01-16",
                            "2021-12-16")

print (stock_data)

# the result set should come back pre-sorted, so i'm grabbing the top one.
smac_res = smac(stock_data).iloc[0]
smac_res.cust_name='SMAC'
rsi_res = rsi(stock_data).iloc[0]
rsi_res.cust_name='RSI'
bnh_res = buy_and_hold(stock_data).iloc[0]
bnh_res.cust_name='BuyNHold'
stoch_hybrid_res = stochastic_smac_hybrid(stock_data, stratOptions={
                        'length': 1,
                        'smoothK': 1,
                        'smoothD': 5,
                        'upperBound': 64,
                        'lowerBound': 44
                    }).iloc[0]
# stoch_hybrid_res = optimize_stochastic_smac_hybrid_results(stock_data)
# try:
#     stoch_hybrid_res.sort(key=lambda x: x.final_value, reverse=True)
# except:
#     print("Not an Array, can't sort")
stoch_hybrid_res.cust_name='Stochastic Smac Hybrid'
# stoch_hybrid_red.iloc[0]
print_sorted_results([smac_res,
                    rsi_res,
                    bnh_res,
                    stoch_hybrid_res])
