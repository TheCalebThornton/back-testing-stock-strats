# back-testing-stock-strats
Simple repo of Python scripts that back test custom trading strategies. Focus on Crypto and S&amp;P500 markets.

# To run the porgram:  
Works best on Python 3.9
### Without Prophet
py -m pip install fastquant  
Navigate to project: py src/crypto/file_name_example.py  
### Running with Prophet:
Disclaimer! Running pystan on Windows is really hard... I don't recommend trying to run /prophet scripts on Windows.  
Instead, you can run this on a Linux or Mac.  
Follow Prophet installation details here: https://facebook.github.io/prophet/docs/installation.html  
I have included some helpful scripts for testing your installation in /testing_pystan_install  

# open source library usage tree
https://github.com/enzoampil/fastquant  
---https://github.com/ccxt/ccxt/tree/master/python/ccxt (fastquant uses this repo to get crypto info)  
---https://github.com/mementum/backtrader (fastquant forked this repo)  
https://github.com/facebook/prophet  

# Main Goal
Discover optimal algorithms for Crypto markets  

# Current Tasks
#### Implement a custom Stochastic SMAC algorithm and backtest it.  
- [x] Add a function that will find optimal parameters across multiple time frames
- [ ] Add partial buys (ie. 60% buy first signal, 40% buy second signal)
- [ ] Add short position testing
#### Implement a backtesting sequence that accurately tests using 'prophet' package to advise investments  
- [ ] Challenge: I have to 'fit' the AI on historical stock data. Then RE-FIT the model for each day we make a trade/signal.
- [ ] Challenge2: Need to exclude holidays and weekends from the predicitions  

# Backtesting Pitfalls
*Overfitting*  
This refers to the situation where the “optimal parameters” that you derived were fit too much to the patterns of a previous time period. This means that the expected profitability of your strategy will not translate to actual profitability in the future when you decide to use it.  
Safeguard against this by using multiple ranges of data sets. Fit to a particular range (ie 2005-2010) then test against multiple ranges (ie 2000-2020, 2000-2009, etc). Depending on the strategy goal, you can test against multiple tickers.

*Look ahead bias*  
This is the bias that results from utilizing information during your backtest that would not have been available during the time period being tested.
This can surface via a programming error or a test range error. Programming error might look like using a strategy that uses 'future' values when determining a trade signal. A test range error could be choosing a specific ticker or year range that appeals to the particular strategy.  

# Additional Resources for Backtesting
https://towardsdatascience.com/backtest-your-trading-strategy-with-only-3-lines-of-python-3859b4a4ab44
