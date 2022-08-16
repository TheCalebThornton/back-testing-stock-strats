import numpy as np
import pandas as pd
import os
# Example Usage:
# stock_data_1 = get_stock_data(ticker,
#                             "2021-12-01",
#                             "2022-08-15")
# stock_data_2 = get_stock_data(ticker,
#                             "2020-12-01",
#                             "2021-08-15")
# optimize_trading_strategy([stock_data_1, stock_data_2], stochastic_smac_hybrid, {
#                                                               lengths: [1,2,3],
#                                                               smoothKs: [1,2,3],
#                                                               smoothKs: [1,2,3],
#                                                               upperBounds: [1,2,3],
#                                                               lowerBounds: [1,2,3]
#                                                               }
# )
def optimize_trading_strategy (stockDataFrames, tradingStrategyFn, tradingStratParams):
    # for attr, val in tradingStratParams.items():
    #     print(attr, val)


    def get_avg_on_column (iterable, property):
        sum = 0.0
        for item in iterable:
            sum = sum + item[property]
        return sum / len(iterable)

    # TODO Need to figure out how to meshgrid tradingStratParams and short options
    allPossibleCombos = np.array(np.meshgrid(tradingStratParams.items().push([True, False]))).T.reshape(-1,6)
    print(allPossibleCombos)
    return true
    runningResults = []

    for optionSet in allPossibleCombos:
        runningOptionResults = []
        # TODO map the optionSet values with the names from 'tradingStratParams' object. Cannot assume index values here.
        options_parsed = {
            'length': optionSet[0],
            'smoothK': optionSet[1],
            'smoothD': optionSet[2],
            'upperBound': optionSet[3],
            'lowerBound': optionSet[4]
        }
        backtest_options_parsed = {
            'allow_short': optionSet[5]
        }

        for stockData in stockDataFrames:
            all_temp_res, hist = tradingStrategyFn(stockData, stratOptions=options_parsed, backtestOptions=backtest_options_parsed)
            temp_res = all_temp_res.iloc[0]
            temp_res['stoch_hybrid_print'] = True
            temp_res['custom_opts'] = options_parsed
            runningOptionResults.append(temp_res)

        resultSetForStockFrames = pd.DataFrame(data={
            'strat_config': f'{options_parsed}',
            'backtest_config': f'{backtest_options_parsed}',
            'average_gain': get_avg_on_column(runningOptionResults, 'pnl'),
            'average_win_rate': get_avg_on_column(runningOptionResults, 'win_rate'),
            'average_total_trades': get_avg_on_column(runningOptionResults, 'total')
        }, index=[0])
        runningResults.append(resultSetForStockFrames)

    for res in runningResults:
        # Outputs to {home}/Documents/optimizer_out_test.csv
        file_path = os.path.join(os.path.expanduser('~'),'Documents','optimizer_out.csv')
        if not os.path.isfile(file_path):
           res.to_csv(file_path)
        else: # else file exists so append without writing the header
           res.to_csv(file_path, mode='a', header=False)

    return runningResults
