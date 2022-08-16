from fastquant import get_stock_data, backtest
import sys
import os
# Python imports are super annoying - modify this path with your own
sys.path.append(os.path.abspath("/Users/cthornton/devl/workspace/back-testing-stock-strats"))
from src.utils.strategies import *

ticker = "TQQQ"
cashToTrade = 10000
stock_data = get_stock_data(ticker,
                            "2021-12-01",
                            "2022-08-15")
print (stock_data)

# the result set should come back pre-sorted, so i'm grabbing the top one.
smac_res = smac(stock_data).iloc[0]
smac_res.cust_name='SMAC'
rsi_res, rsi_hist = rsi(stock_data, backtestOptions={'return_history': True, 'allow_short': True})
rsi_res = rsi_res.iloc[0]
rsi_res.cust_name = "RSI"
bnh_res = buy_and_hold(stock_data).iloc[0]
bnh_res.cust_name='BuyNHold'

stoch_hybrid_res, stoch_hybrid_hist = stochastic_smac_hybrid(stock_data,
                                                            stratOptions={'length': 1, 'smoothK': 4, 'smoothD': 4, 'upperBound': 65, 'lowerBound': 45},
                                                            backtestOptions={'allow_short':True})
stoch_hybrid_res = stoch_hybrid_res.iloc[0]
stoch_hybrid_res.cust_name='Stochastic Smac Hybrid 1,4,4'

stoch_hybrid_res_2, stoch_hybrid_hist_2 = stochastic_smac_hybrid(stock_data,
                                                            stratOptions={'length': 1, 'smoothK': 4, 'smoothD': 2, 'upperBound': 65, 'lowerBound': 45},
                                                            backtestOptions={'allow_short':True})
stoch_hybrid_res_2 = stoch_hybrid_res_2.iloc[0]
stoch_hybrid_res_2.cust_name='Stochastic Smac Hybrid 1,4,2'

print_sorted_results([stoch_hybrid_res, stoch_hybrid_res_2, bnh_res, smac_res, rsi_res])
# Print History
for key, value in rsi_hist.items():
    file_path = os.path.join(os.path.expanduser('~'),'Documents','nyse_sample.csv')
    value.to_csv(file_path, mode='a', header=True)
print("history result written to Documents/nyse_sample.csv")
# df_hist = pd.DataFrame.from_dict(stoch_hybrid_hist, orient='index')
# stoch_hybrid_hist.items()[0].to_csv('src/testing_results/nyse_sample.csv')
