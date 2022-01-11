from fastquant import backtest
import backtrader as bt
import numpy as np
import pandas as pd
import os

# results is a list of each strats' top result
def print_sorted_results(results, verbose=False):
    try:
        results.sort(key=lambda x: x.final_value, reverse=True)
    except:
        print("Not an Array, can't sort")
    print ('BEST RESULTS IN ORDER DESC:')
    for result in results:
        strat_name =  getattr(result, 'cust_name', 'N/A')
        print(f'{strat_name}')
        if verbose :
            print('VERBOSE INFORMATION:')
            print(f'{result}')
        else:
            init_cash = getattr(result, 'init_cash', None)
            final_value = getattr(result, 'final_value', None)
            pnl = getattr(result, 'pnl', None)
            total_trades = getattr(result, 'total', None)
            win_rate = getattr(result, 'win_rate', 1)
            # accomdate various parameters for individual strats
            prcntGain = (final_value / init_cash - 1) * 100
            print (f'initial_cash: {init_cash}. final_cash: {final_value}. Percentage Gain: {prcntGain}. Total Profit: {pnl}. Total Trades: {total_trades}. Win Rate: {win_rate}')

        if getattr(result, 'stoch_hybrid_print', False):
            custOpts = getattr(result, 'custom_opts', 'N/A')
            print ('BEST CONFIGURATION PARAMS:')
            print (f'Stoch Hybrid Options: {custOpts}\n')
        else:
            param1 = getattr(result, 'fast_period', getattr(result, 'rsi_upper', getattr(result, 'upper_limit', None)))
            param2 = getattr(result, 'slow_period', getattr(result, 'rsi_lower', getattr(result, 'lower_limit', None)))
            param3 = getattr(result, 'rsi_period', None)
            print ('BEST CONFIGURATION PARAMS:')
            print (f'param1: {param1}. param2: {param2}. param3: {param3} \n')

def smac (dataSet, initCash=10000, backtestOptions={}):
    return backtest('smac',
       dataSet,
       init_cash=initCash,
       fast_period=[7,14,21,28],
       slow_period=[30,45,60,75],
       plot=getattr(backtestOptions, 'plot', False),
       verbose=getattr(backtestOptions, 'verbose', False)
      )

def macd (dataSet, initCash=10000, backtestOptions={}):
  return backtest('macd',
     dataSet,
     init_cash=initCash,
     fast_period=[12],
     slow_period=[26],
     signal_period=[9],
     sma_period=[30],
     dir_period=[10],
     plot=getattr(backtestOptions, 'plot', False),
     verbose=getattr(backtestOptions, 'verbose', False)
    )

def rsi (dataSet, initCash=10000, backtestOptions={}):
     return backtest('rsi',
         dataSet,
         init_cash=initCash,
         rsi_upper=[75, 64],
         rsi_lower=[40, 44],
         rsi_period=[14, 5, 20],
         plot=getattr(backtestOptions, 'plot', False),
         verbose=getattr(backtestOptions, 'verbose', False)
        )

def buy_and_hold (dataSet, initCash=10000, backtestOptions={}):
    return backtest('buynhold',
       dataSet,
       init_cash=initCash,
       plot=getattr(backtestOptions, 'plot', False),
       verbose=getattr(backtestOptions, 'verbose', False)
    )



def stochastic_smac_hybrid (dataFrame, initCash=10000,
                            backtestOptions={},
                            stratOptions={
                                'length': 1,
                                'smoothK': 4,
                                'smoothD': 4,
                                'upperBound': 64,
                                'lowerBound': 44
                            }):
    def add_data_points (dataFrame):
        def get_average (prices):
            sum = 0.0
            for price in prices:
                sum = sum + price
            return sum / len(prices)

        def stoch (close, highest, lowest):
            return 100 * (close - lowest) / (highest - lowest)

        def get_previous_rows_safe (dataFrame, index, columnName, total):
            def single_value (target):
                return dataFrame.at[target, columnName]
            rows = []
            for n in range(0, total):
                if (not (index-n < 0)):
                    rows.append(single_value(index-n))
            return rows

        def getCrossUp (kLineCross, dLineCross, prevK, prevD):
            return True if (prevK < prevD and prevK < stratOptions['lowerBound']) and (kLineCross > dLineCross) else False
        def getCrossDown (kLineCross, dLineCross, prevK, prevD):
            return True if (prevK > prevD and prevK > stratOptions['upperBound']) and (kLineCross < dLineCross) else False

        newFrame = dataFrame.copy().reset_index()
        newFrame['stoch_low'] = newFrame['low'].rolling(stratOptions['length']).min()
        newFrame['stoch_high'] = newFrame['high'].rolling(stratOptions['length']).max()
        newFrame['stoch_temp'] = stoch(newFrame['close'], newFrame['stoch_high'], newFrame['stoch_low'])
        for i, row in newFrame.iterrows():
            kLine = get_average(get_previous_rows_safe(newFrame, i, 'stoch_temp', stratOptions['smoothK']))
            newFrame.at[i, '%K'] = kLine
            dLine = get_average(get_previous_rows_safe(newFrame, i, '%K', stratOptions['smoothD']))
            newFrame.at[i, '%D'] = dLine
            x_up = getCrossUp(kLine, dLine,
                                get_previous_rows_safe(newFrame, i, '%K', 2)[-1],
                                get_previous_rows_safe(newFrame, i, '%D', 2)[-1])
            x_down = getCrossDown(kLine, dLine,
                                get_previous_rows_safe(newFrame, i, '%K', 2)[-1],
                                get_previous_rows_safe(newFrame, i, '%D', 2)[-1])
            newFrame.at[i, 'signal'] = 1 if x_up else -1 if x_down else 0
        return newFrame

    verboseDataFrame = add_data_points(dataFrame)
    stratData = dataFrame.copy()
    stratData['custom'] = verboseDataFrame['signal'].values
    filtered_data = verboseDataFrame.loc[(verboseDataFrame['signal'] != 0)]
    print(f'Signals: {filtered_data}')
    # print(f'Modified Strat Data: {stratData}')
    custom_res, history = backtest('custom',
                     stratData,
                     init_cash=initCash,
                     upper_limit=[0.9],
                     lower_limit=[-0.9],
                     plot=getattr(backtestOptions, 'plot', False),
                     verbose=getattr(backtestOptions, 'verbose', False),
                     return_history=True
                    )
    return custom_res

#DEPRECATED - This has been moved to be more generic of an impl
def optimize_stochastic_smac_hybrid_results (stockDataFrames):
    lengths = [1,2,3]
    smoothKs = [1,2,3,4,5,6]
    smoothDs = [1,2,3,4,5,6]
    upperBounds = [65, 80]
    lowerBounds = [45, 20]

    def get_avg_on_column (iterable, property):
        sum = 0.0
        for item in iterable:
            sum = sum + item[property]
        return sum / len(iterable)

    allPossibleCombos = np.array(np.meshgrid(lengths,smoothKs,smoothDs,upperBounds,lowerBounds)).T.reshape(-1,5)
    runningResults = []

    for optionSet in allPossibleCombos:
        runningOptionResults = []
        options_parsed = {
            'length': optionSet[0],
            'smoothK': optionSet[1],
            'smoothD': optionSet[2],
            'upperBound': optionSet[3],
            'lowerBound': optionSet[4]
        }
        for stockData in stockDataFrames:
            temp_res = stochastic_smac_hybrid(stockData, stratOptions=options_parsed).iloc[0]
            temp_res['stoch_hybrid_print'] = True
            temp_res['custom_opts'] = options_parsed
            runningOptionResults.append(temp_res)
        resultSetForStockFrames = pd.DataFrame(data={
            'configuration': f'{options_parsed}',
            # 'results': runningOptionResults,
            'average_gain': get_avg_on_column(runningOptionResults, 'pnl'),
            'average_win_rate': get_avg_on_column(runningOptionResults, 'win_rate'),
            'average_total_trades': get_avg_on_column(runningOptionResults, 'total')
        }, index=[0])
        runningResults.append(resultSetForStockFrames)

    for res in runningResults:
        file_path = 'src/testing_results/optimizerResults.csv'
        if not os.path.isfile(file_path):
           res.to_csv(file_path)
        else: # else it exists so append without writing the header
           res.to_csv(file_path, mode='a', header=False)

    return runningResults
