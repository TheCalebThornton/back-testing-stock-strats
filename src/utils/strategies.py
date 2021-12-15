from fastquant import backtest
import backtrader as bt

# results is a list of each strats' top result
def print_sorted_results(results, verbose=False):
    try:
        results.sort(key=lambda x: x.final_value, reverse=True)
    except:
        print("Not an Array, can't sort")
    print ('BEST RESULTS IN ORDER DESC:')
    for result in results:
        strat_name =  getattr(result, 'cust_name', None)
        print(f'{strat_name}')
        if verbose :
            print('VERBOSE INFORMATION:')
            print(f'{result}')
        else:
            init_cash = getattr(result, 'init_cash', None)
            final_value = getattr(result, 'final_value', None)
            pnl = getattr(result, 'pnl', None)
            total_trades = getattr(result, 'total', None)
            # accomdate various parameters for individual strats
            param1 = getattr(result, 'fast_period', getattr(result, 'rsi_upper', getattr(result, 'upper_limit', None)))
            param2 = getattr(result, 'slow_period', getattr(result, 'rsi_lower', getattr(result, 'lower_limit', None)))
            param3 = getattr(result, 'rsi_period', None)
            prcntGain = (final_value / init_cash - 1) * 100
            print (f'initial_cash: {init_cash}. final_cash: {final_value}. Percentage Gain: {prcntGain}. Total Profit: {pnl}. Total Trades: {total_trades}')
            print ('BEST CONFIGURATION PARAMS:')
            print (f'param1: {param1}. param2: {param2}. param3: {param3} \n')

def smac (dataSet, initCash=10000, plot=False, verbose=False):
    return backtest('smac',
       dataSet,
       init_cash=initCash,
       fast_period=[7,14,21,28],
       slow_period=[30,45,60,75],
       plot=plot,
       verbose=verbose
      )

def rsi (dataSet, initCash=10000, plot=False, verbose=False):
     return backtest('rsi',
         dataSet,
         init_cash=initCash,
         rsi_upper=[75, 64],
         rsi_lower=[40, 44],
         rsi_period=[14, 5, 20],
         plot=plot,
         verbose=verbose
        )

def buy_and_hold (dataSet, initCash=10000, plot=False, verbose=False):
    return backtest('buynhold',
       dataSet,
       init_cash=initCash,
       plot=plot,
       verbose=verbose
    )



def stochastic_smac_hybrid (dataFrame, initCash=10000, plot=False, verbose=False):
    # Stochastic algo
    length = 1
    smoothK = 4
    smoothD = 4
    upperBound = 64
    lowerBound = 44
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
            return True if (prevK < prevD and prevK < lowerBound) and (kLineCross > dLineCross) else False
        def getCrossDown (kLineCross, dLineCross, prevK, prevD):
            return True if (prevK > prevD and prevK > upperBound) and (kLineCross < dLineCross) else False

        newFrame = dataFrame.copy().reset_index()
        newFrame['stoch_low'] = newFrame['low'].rolling(length).min()
        newFrame['stoch_high'] = newFrame['high'].rolling(length).max()
        newFrame['stoch_temp'] = stoch(newFrame['close'], newFrame['stoch_high'], newFrame['stoch_low'])
        for i, row in newFrame.iterrows():
            kLine = get_average(get_previous_rows_safe(newFrame, i, 'stoch_temp', smoothK))
            newFrame.at[i, '%K'] = kLine
            dLine = get_average(get_previous_rows_safe(newFrame, i, '%K', smoothD))
            newFrame.at[i, '%D'] = dLine
            x_up = getCrossUp(kLine, dLine,
                                get_previous_rows_safe(newFrame, i, '%K', 2)[-1],
                                get_previous_rows_safe(newFrame, i, '%D', 2)[-1])
            x_down = getCrossDown(kLine, dLine,
                                get_previous_rows_safe(newFrame, i, '%K', 2)[-1],
                                get_previous_rows_safe(newFrame, i, '%D', 2)[-1])
            newFrame.at[i, 'signal'] = 1 if x_up else -1 if x_down else 0
        return newFrame

    new_frame = add_data_points(dataFrame)


    # new_frame = add_data_points(dataFrame)

    # newData = dataSet["custom"] = ''
    # newData = dataSet
    filtered_data = new_frame.loc[(new_frame['signal'] != 0)]
    print (f'Stock data: {dataFrame}')
    print(f'Signals: {filtered_data}')
    print(f'Modified Data: {new_frame}')
    # custom_res, history = backtest('custom',
    #                  newData,
    #                  init_cash=initCash,
    #                  upper_limit=[1],
    #                  lower_limit=[-1],
    #                  plot=plot,
    #                  verbose=verbose,
    #                  return_history=True
    #                 )
    # return custom_res
