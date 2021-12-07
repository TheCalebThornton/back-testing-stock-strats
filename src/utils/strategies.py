from fastquant import backtest

# results is a list of each strats' top result
def print_sorted_results(results, verbose=False):
    results.sort(key=lambda x: x.final_value, reverse=True)
    print ('BEST RESULTS IN ORDER DESC:')
    for result in results:
        strat_name =  getattr(result, 'cust_name', None)
        print(f'{strat_name}')
        if verbose :
            print('VERBOSE INFORMATION:')
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
       plot=False,
       verbose=False
      )

def rsi (dataSet, initCash=10000, plot=False, verbose=False):
     return backtest('rsi',
         dataSet,
         init_cash=initCash,
         rsi_upper=[75, 65],
         rsi_lower=[40, 35],
         rsi_period=[10,14],
         plot=False,
         verbose=False
        )

def buy_and_hold (dataSet, initCash=10000, plot=False, verbose=False):
    return backtest('buynhold',
       dataSet,
       init_cash=initCash,
       plot=False,
       verbose=False
    )

# stock_data["custom"] = stock_data.close.pct_change()
# custom_res, history = backtest('custom',
#                  stock_data,
#                  init_cash=cashToTrade,
#                  upper_limit=[0.05, 0.07, 0.5],
#                  lower_limit=[0.03, 0.01, 0.005],
#                  plot=False,
#                  verbose=False,
#                  return_history=True
#                 )
