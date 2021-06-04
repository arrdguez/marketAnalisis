#!/usr/bin/python3

import pandas as pd
from finta import TA


import sys
sys.path.insert(1, '../')
from exchange.binance import Binance
from strategies.strategies import Strategies
from plot.plot import chart
#import exchange

from core.SMI import smiHistogram


class tradeSigns():
  """
    docstring for tradeSigns

  """
  def __init__(self):
    self.exchange = Binance()
    self.chart = chart()
    self.SMIH = smiHistogram()


    self.param = [{"col_name" : "4_ema", 
                   "color"    : 'green', 
                   "name"     : "4_ema"},
                  {"col_name" : "9_ema", 
                   "color"    : 'yellow', 
                   "name"     : "9_ema"},
                  {"col_name" : "18_ema", 
                   "color"    : "red", 
                   "name"     : "18_ema"}]
    self.TLSR = []

  def sign(self, symbol:str, timeframe:str):
    """



    """

    df = self.exchange.GetSymbolKlines(symbol = symbol, interval = timeframe)
    df = self.technicalAnalsis(df)
    dfSlope = self.slopCalculator(df)
    dfResult = pd.DataFrame(columns=['time','result', 'resultCode','date'])
    
    #print(df)
    #print(dfSlope)
    #exit()
    df["sign"] = ""
    entrypoint = 'off'
    listResult = []
    for i in range(2, len(df['close'])-1):

      strategy_result = Strategies.tlStrategyTWO(df = df, dfSlope=dfSlope, step = i)
      listResult.append(strategy_result)
      self.TLSR.append([df['time'][i], strategy_result,    df['high'][i]])


    df.to_csv("df.csv", sep='\t')
    dfSlope.to_csv("slope.csv", sep='\t')
    #print(listResult)
    #print(dfResult)

    self.chart.plotData(df, symbol, timeframe, self.param, self.TLSR)

  def technicalAnalsis(self, df):
    df['10_ema'] = TA.EMA(df, 10)
    df['55_ema'] = TA.EMA(df, 55)

    #ADX
    df["ADX"] = TA.ADX(df)
    df["ADX"] = df["ADX"].fillna(0)

    #QMI
    df['SMIH'] = self.SMIH.SMIH(df)


    return df

  def slopCalculator(self, df):
    i = 3
    dfSlope = pd.DataFrame(columns=['adxSlope', 'histSlope', 'adxStatus'])
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

      if df['SMIH'][i] < df['SMIH'][i-1]:
        histSlope = -1
      elif df['SMIH'][i] > df['SMIH'][i-1]:
        histSlope = 1
      dfSlope.loc[i, 'adxSlope'] = adxSlope
      dfSlope.loc[i, 'histSlope'] = histSlope
      dfSlope.loc[i, 'adxStatus'] = adxStatus

    return dfSlope



def Main():

  ts = tradeSigns()
  ts.sign("BTCUSDT", "1h")


if __name__ == '__main__':
  Main()

