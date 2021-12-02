# back-testing-stock-strats
Simple repo of Python scripts that back test custom trading strategies. Focus on Crypto and S&amp;P500 markets.

# open source library usage tree
https://github.com/enzoampil/fastquant  
---https://github.com/ccxt/ccxt/tree/master/python/ccxt (fastquant uses this repo to get crypto info)  
---https://github.com/mementum/backtrader (fastquant forked this repo)

# Stochastic alogrithm
https://www.tradingview.com/pine-script-reference/v1/#fun_stoch
100 * (close - lowest(low, length)) / (highest(high, length) - lowest(low, length)).
Ex. sma(stoch(close, high, low, len), smoothK)

# Goal 1
Test Stochastic trading strat against Crypto markets  

# Goal 2
Test Stochastic trading strat against any S&P500 Ticker  

# Backtesting Pitfalls
*Overfitting*  
This refers to the situation where the “optimal parameters” that you derived were fit too much to the patterns of a previous time period. This means that the expected profitability of your strategy will not translate to actual profitability in the future when you decide to use it.  
Safeguard against this by using multiple ranges of data sets. Fit to a particular range (ie 2005-2010) then test against multiple ranges (ie 2000-2020, 2000-2009, etc). Depending on the strategy goal, you can test against multiple tickers.

*Look ahead bias*  
This is the bias that results from utilizing information during your backtest that would not have been available during the time period being tested.
This can surface via a programming error or a test range error. Programming error might look like using a strategy that uses 'future' values when determining a trade signal. A test range error could be choosing a specific ticker or year range that appeals to the particular strategy.  

# Additional Resources for Backtesting
https://towardsdatascience.com/backtest-your-trading-strategy-with-only-3-lines-of-python-3859b4a4ab44
