# pip install tinkoff-investments

# Переключение между контурами реализовано через target, INVEST_GRPC_API - "боевой"
# , INVEST_GRPC_API_SANDBOX - "песочница"

# песочница
token = ''

from tinkoff.invest import Client
from tinkoff.invest.constants import INVEST_GRPC_API, INVEST_GRPC_API_SANDBOX

import numpy as np
import pandas as pd
import requests 
import json

import matplotlib.pyplot as plt




ticker = 'sber'
board = 'tqbr'

start_interval = '2020-01-01'
end_interval = '2023-11-01'
period = 'D' #'1m', '10m', '1h', 'D', 'W', 'M', 'Q' 

cash = 10000

position = 0
fee = 0.0004





# window_size = 10
strategy=MeanReversion(10, fee)

##### ticker+board -> figi for Tinkoff API
def get_share_attributes(TOKEN=token, ticker='SBER', board='TQBR'):
    
    ticker = ticker.upper()
    board = board.upper()

    with Client(TOKEN, target=INVEST_GRPC_API_SANDBOX) as client:

        instr = client.instruments.share_by(id_type=2, class_code=board, id=ticker)
        
        itg = []

        itg.append(instr.instrument.figi )
        itg.append(instr.instrument.isin )
        itg.append(instr.instrument.ticker )
        itg.append(instr.instrument.class_code )
        itg.append(instr.instrument.lot )
        itg.append(instr.instrument.currency )
        
        return itg

#algoPack
    #чтобы доставать торг инфу
import pandas as pd
from moexalgo import Ticker, Market

def get_shares_candles(secs=[], start = '2020-01-01', end = '2023-11-01', period='D'): 

    x = pd.DataFrame()

    for i in secs:
        try:
            ticker = Ticker(i.upper())
            y = ticker.candles(date=start, till_date=end, period=period)
            y['ticker'] = i
            x = pd.concat([x , y], axis=0)
        except:
            pass
    return x



def strat_back_test(strategy=strategy
                   , ticker=ticker
                   , board=board
                    
                   , start=start_interval
                   , end=end_interval
                   , period=period
                   
                   , cash=cash
                   , position=position
                   , fee=fee
                   
                   , plot=False):
    
    
    
    df = get_shares_candles(secs=[ticker]
                   , start = start_interval
                   , end = end_interval
                   , period=period)
    
    #strategy = MeanReversion(10, 0.0004)

    
    logs = []
    shares_quant = []
    pnl_logs = []
    
    
    for i, row in df.iterrows():
        update = {'price': row['close']}
        delta_position = strategy.get_update(update)
        position += delta_position

        shares_quant.append(position)
        logs.append(delta_position)

        if delta_position == 0:
            pass
        elif delta_position > 0:
            cash -= delta_position*(row['close']*(1+strategy.fees))
        else:
            cash += delta_position*(row['close']*(1-strategy.fees))

        pnl_logs.append(cash+position*row['close'])
        
    
    meta = { 'data': df   #candles data
        , 'basic': {'ticker': ticker #ticker
                      , 'board':board} #board
            , 'strategy_params': {'start': start
                                  , 'end': end
                                  , 'period': period} #timeframe of data
             
            , 'portfolio_params': {'cash': cash #start RUB summ 
                                   , 'position': position #start ammount of stocks
                                   , 'fee': fee} #comission
            , 'itg_strategy_meta': {'our_trades': logs #1 - buy, 0 - nothing, -1 sell
                                    , 'quant_change': shares_quant #ammount of stocks
                                    ,'cash_change': pnl_logs } #profit n losses
           }
    
    if plot==True:
        plt.plot(pnl_logs)
        
    return meta



