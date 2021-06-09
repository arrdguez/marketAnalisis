#!/usr/bin/python3

import pandas as pd
from finta import TA

import time
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
    self.TLSR = [[1622313900000.0, '0', 34110.5],[1622313900000.0, '0', 34110.5],[1622313900000.0, '0', 34110.5]]
    self.indicatorMap = {"0a" : "",
                             "0b" : "",
                             "0c" : "",
                             "0d" : "",
                             "1a" : "",
                             "1b" : "",
                             "1c" : "",
                             "1d" : "",
                             "2a" : "",
                             "2b" : "",
                             "2c" : "",
                             "2d" : "",
                             "3a" : "",
                             "3b" : "",
                             "3c" : "",
                             "3d" : ""}

    self.indicatorMapVerbose = {"0a" : "",
                                    "0b" : "",
                                    "0c" : "",
                                    "0d" : "",
                                    "1a" : "",
                                    "1b" : "",
                                    "1c" : "",
                                    "1d" : "",
                                    "2a" : "",
                                    "2b" : "",
                                    "2c" : "",
                                    "2d" : "",
                                    "3a" : "",
                                    "3b" : "",
                                    "3c" : "",
                                    "3d" : ""}






  def sign(self, symbol:str, timeframe:str):
    """



    """

    df = self.exchange.GetSymbolKlines(symbol = symbol, interval = timeframe)
    df = self.technicalAnalsis(df)
    dfSlope = self.slopCalculator(df)
    dfResult = pd.DataFrame(columns=['time','result', 'resultCode','date'])
    print(df)


    entrypoint = 'off'
    listResult = []
    for i in range(2, len(df['close'])-1):

      strategy_result = Strategies.tlStrategyTWO(df = df, dfSlope=dfSlope, step = i)
      print(strategy_result)
      listResult.append(strategy_result)
      self.TLSR.append([df['time'][i], strategy_result, df['high'][i]])
      df.loc[i, 'signal'] = str(strategy_result)

    print(len(self.TLSR))
    print(len(df))

    df.to_csv("df.csv", sep='\t')
    dfSlope.to_csv("slope.csv", sep='\t')
    #print(listResult)
    #print(dfResult)
    exit()
    self.chart.plotData(df, symbol, timeframe, self.param, self.TLSR)


  def analitic(self, symbol:str, timeframe:str):
    """



    """
    steps = 30000
    count = int (0)
    while count <= steps:
      count += 1
      

      df15m = self.exchange.GetSymbolKlines(symbol = symbol, interval = "15m")#, limit = 250)
      df15m = self.technicalAnalsis(df15m)
      dfSlope15m = self.slopCalculator(df15m)

      df5m = self.exchange.GetSymbolKlines(symbol = symbol, interval = "5m")#, limit = 250)
      df5m = self.technicalAnalsis(df5m)
      dfSlope5m = self.slopCalculator(df5m)

      #print(df5m)
      #print(type(df5m))
      #print(len(df5m['close'])-1)


      #print(dfSlope5m)
      #print(type(dfSlope5m))
      #print(len(dfSlope5m['adxSlope'])-1)

      #exit()
      strategy_result5m = Strategies.tlStrategyLiveLong(df = df5m, dfSlope=dfSlope5m, step = len(df5m['close'])-1)
      strategy_result5mprev = Strategies.tlStrategyLiveLong(df = df5m, dfSlope=dfSlope5m, step = len(df5m['close'])-2)


      strategy_result15m = Strategies.tlStrategyLiveLong(df = df15m, dfSlope=dfSlope15m, step = len(df15m['close'])-1)
      strategy_result15mprev = Strategies.tlStrategyLiveLong(df = df15m, dfSlope=dfSlope15m, step = len(df15m['close'])-2)


      print("Parameter              5m              15m")
      print("indicator              "+str(strategy_result5m)+"              "+str(strategy_result15m))
      print("indicatorPre           "+str(strategy_result5mprev)+"              "+str(strategy_result15mprev))

      time.sleep(30)

  def technicalAnalsis(self, df):
    df['10_ema'] = TA.EMA(df, 10)
    df['55_ema'] = TA.EMA(df, 55)


    #ADX
    df["ADX"] = self.SMIH.ADX(df)
    df["ADX"] = df["ADX"].fillna(0)
    df = df.drop(columns=['plus','minus','sum','tmp', 'up', 'down', 'TR', 'truerange'])


    #QMI
    df['SMIH'] = self.SMIH.SMIH(df)


    return df

  def slopCalculator(self, df):
    i = 3
    dfSlope = pd.DataFrame(columns=['adxSlope', 'histSlope', 'adxStatus'])
    dfSlope.loc[0] = 0
    dfSlope.loc[1] = 0
    for i in range(2, len(df['close'])):
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
  #ts.sign("BTCUSDT", "5m")
  ts.analitic("BTCUSDT", "5m")


if __name__ == '__main__':
  Main()

