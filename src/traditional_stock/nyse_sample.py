from fastquant import get_stock_data, backtest
from src.utils.strategies import *

ticker = "TQQQ"
cashToTrade = 10000
stock_data = get_stock_data(ticker,
                            "2021-12-25",
                            "2022-01-29")
print (stock_data)

# the result set should come back pre-sorted, so i'm grabbing the top one.
# smac_res = smac(stock_data).iloc[0]
# smac_res.cust_name='SMAC'
# rsi_res = rsi(stock_data).iloc[0]
# rsi_res.cust_name='RSI'
bnh_res = buy_and_hold(stock_data).iloc[0]
bnh_res.cust_name='BuyNHold'
stoch_hybrid_res, stoch_hybrid_hist = stochastic_smac_hybrid(stock_data, stratOptions={'length': 1, 'smoothK': 4, 'smoothD': 2, 'upperBound': 65, 'lowerBound': 45})
stoch_hybrid_res = stoch_hybrid_res.iloc[0]
stoch_hybrid_res.cust_name='Stochastic Smac Hybrid'

print_sorted_results([stoch_hybrid_res, bnh_res])
# Print History
# for key, value in stoch_hybrid_hist.items():
#     print(key, ' : ', type(value))
#     value.to_csv('src/testing_results/nyse_sample.csv', mode='a', header=True)
# df_hist = pd.DataFrame.from_dict(stoch_hybrid_hist, orient='index')
# stoch_hybrid_hist.items()[0].to_csv('src/testing_results/nyse_sample.csv')
