#!/usr/bin/python3

import pandas as pd
from finta import TA


import sys
sys.path.insert(1, '../')
from exchange.binance import Binance
from strategies.strategies import Strategies
from plot.plot import chart
#import exchange


class tradeSigns():
  """
    docstring for tradeSigns

  """
  def __init__(self):
    self.exchange = Binance()
    self.chart = chart()


    self.param = [{"col_name" : "4_ema", 
                   "color"    : 'green', 
                   "name"     : "4_ema"},
                  {"col_name" : "9_ema", 
                   "color"    : 'yellow', 
                   "name"     : "9_ema"},
                  {"col_name" : "18_ema", 
                   "color"    : "red", 
                   "name"     : "18_ema"}]
    self.buy_signals = []
    self.sell_signals = []

  def sign(self, symbol:str, timeframe:str):
    """



    """

    df = self.exchange.GetSymbolKlines(symbol = symbol, interval = timeframe)
    #df = self.exchange.technicalA(df)

    df['3_ema'] = TA.EMA(df, 3)
    df['25_sma'] = TA.SMA(df, 25)
    #df['10_ema'] = TA.EMA(df, 10)
    #df['55_ema'] = TA.EMA(df, 55)

    #df2= TA.MACD(df = df, period_fast = 30, period_slow = 20, signal = 30)
    df2= TA.MACD(df, period_fast = 30, period_slow = 20, signal = 30)
    df2["HIST"] = df2["MACD"] - df2["SIGNAL"]
    df["MACD"]   = df2["MACD"]
    df["SIGNAL"] = df2["SIGNAL"]
    df["HIST"]   = df2["HIST"]
    df['HIST_ESMA'] = df['3_ema'] - df['25_sma']

    #ADX
    df["ADX"] = TA.ADX(df)
    df["ADX"] = df["ADX"].fillna(0)
    df["HIST_ESMA"] = df["HIST_ESMA"].fillna(0)

    self.slopCalculator(df)

    df.to_csv('./export.csv', sep='\t')
    print(df)
    exit()
    df["sign"] = ""
    entrypoint = 'off'
    for i in range(0, len(df['close'])-1):
      #strategy_result = Strategies.marginTrade(df = df, step = i)
      strategy_result = Strategies.tlStrategy(df = df, step = i)

      if strategy_result['signal'] == 'BUY' and entrypoint == 'off':
        #print('buy: ',i)
        self.buy_signals.append([df['time'][i], df['low'][i]])
        df.loc[i, 'sign'] = 'buy'
        entrypoint = 'on'
      elif strategy_result['signal'] == 'SELL' and entrypoint == 'on':
        #print('sell: ',i)
        df.loc[i, 'sign'] = 'sell'
        self.sell_signals.append([df['time'][i], df['low'][i]])
        
        entrypoint = 'off'

    #print(self.sell_signals)
    self.chart.plotData(df, symbol, timeframe, self.param, self.buy_signals, self.sell_signals)


  def slopCalculator(self, df):
    i = 3
    for i in range(2, len(df['close'])-1):
      adxSlope = 0
      histSlope = 0
      adxStatus = 0

      if df['ADX'][i] < 23:
        adxStatus = 0
      elif df['ADX'][i] > 23:
        adxStatus = 1

      if df['ADX'][i] < df['ADX'][i-1]:
        adxSlope = -1
      elif df['ADX'][i] > df['ADX'][i-1]:
        adxSlope = 1

      if df['HIST_ESMA'][i] < df['HIST_ESMA'][i-1]:
        histSlope = -1
      elif df['HIST_ESMA'][i] > df['HIST_ESMA'][i-1]:
        histSlope = 1

      

      print(str(adxStatus) +"      "+  str(adxSlope) + "     "+ str(histSlope))



def Main():

  ts = tradeSigns()
  ts.sign("BTCUSDT", "5m")


if __name__ == '__main__':
  Main()

