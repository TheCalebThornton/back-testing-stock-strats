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

# WIP - This should look backwards up to 'length' steps away from target
# def sma (source, data_line, length):
#     sum = 0.0
#     for i=0 i<=length-1
#         sum = (sum + source[i])
#     return sum / length

# WIP - lowest and highest should look backwards up to 'length' steps away from target
# def stoch (source, data_line, length):
#     def lowest (source)
#     return 100 * (close - lowest(low, length)) / (highest(high, length) - lowest(low, length))

def stochastic_smac (dataSet, initCash=10000, plot=False, verbose=False):
    # Stochastic algo
    len = 1
    smoothK = 4
    smoothD = 4
    upperBound = 64
    lowerBound = 44
    # kLine = sma(stoch(close, high, low, length), smoothK)
    # dLine = sma(kLine, smoothD)
    # sma(stoch(close, high, low, len), smoothK)
    # newData = dataSet["custom"] = dataSet.close
    # newData = dataSet
    # for row in dataSet:
    #     kLine = sma(stoch(row.close, row.high, row.low, length), smoothK)
    #     dLine = sma(kLine, smoothD)
    #     sma(stoch(close, high, low, len), smoothK)
    #     row.custom = ""
    print(f'Modified Data: {newData}')
    print (f'Stock data: {stock_data}')
    custom_res, history = backtest('custom',
                     newData,
                     init_cash=initCash,
                     upper_limit=[0.05, 0.07, 0.5],
                     lower_limit=[0.03, 0.01, 0.005],
                     plot=plot,
                     verbose=verbose,
                     return_history=True
                    )
    return custom_res
