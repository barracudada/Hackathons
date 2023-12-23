Python 3.11.4 (v3.11.4:d2340ef257, Jun  6 2023, 19:15:51) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin
Type "help", "copyright", "credits" or "license()" for more information.
>>> 
>>> #algoPack
... from moexalgo import Ticker, Market
... 
... def get_shares_candles(secs=[], start = '2020-01-01', end = '2023-11-01', period='D'): 
... 
...     x = pd.DataFrame()
... 
...     for i in secs:
...         try:
...             ticker = Ticker(i)
...             y = ticker.candles(date=start, till_date=end, period=period)
...             y['ticker'] = i
...             x = pd.concat([x , y], axis=0)
...         except:
...             pass
