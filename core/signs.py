#!/usr/bin/python3

import pandas as pd
from finta import TA

import time
import datetime
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
    self.indicatorMap = {"0a" : "(0a) Attention to close",
                         "0b" : "(0b) Attention to close",
                         "0c" : "(0c) Wait to Close",
                         "0d" : "(0d) Wait nothing to do",
                         "1a" : "(1a) Wait for the ADX change to Open",
                         "1b" : "(1b) Wait for the ADX change to Open",
                         "1c" : "(1c) Open",
                         "1d" : "(1d) Open",
                         "2a" : "(2a) Price is drop",
                         "2b" : "(2b) Price is drop",
                         "2c" : "(2c) Close",
                         "2d" : "(2d) Close(if you are inside) or Wait",
                         "3a" : "(3a) Strong drop price",
                         "3b" : "(3b) Strong drop price",
                         "3c" : "(3c) Wait the price can get drop strong",
                         "3d" : "(3d) Wait the price can get drop strong"}

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
    #print(df)


    entrypoint = 'off'
    listResult = []
    
    for i in range(0, len(df['close'])):
      strategy_result = Strategies.tlStrategyTWO(df = df, dfSlope=dfSlope, step = i)

      df.loc[i, 'signal'] = str(strategy_result)
      if strategy_result == "1c" and listResult[-2] != "1c" and listResult[-2] == "3c":
        #print(str(df.loc[i-1,'date'])+"\t"+str(listResult[-2])+"\t"+str(df.loc[i-1,'signal']))

        strategy_result = "1b"

      listResult.append(str(strategy_result))
      self.TLSR.append([df['time'][i], strategy_result, df['high'][i]])

    

    for i in range(0, len(df['close'])):
      print(str(df.loc[i,'date'])+"\t"+str(df.loc[i,'signal'])+"\t"+str(dfSlope.loc[i,'histSlope'])+"\t"+str(dfSlope.loc[i,'adxSlope'])+"\t"+str(dfSlope.loc[i,'adxStatus'])+"\t"+str(df.loc[i,'ADX']))

    print("\nlast strategy result: ", strategy_result)
    print(timeframe)
    print(dfSlope)
    print(len(dfSlope))


    #exit()
    df.to_csv("df.csv", sep='\t')
    dfSlope.to_csv("slope.csv", sep='\t')
    #print(listResult)
    #print(dfResult)
    #exit()
    self.chart.plotData(df, symbol, timeframe, self.param, self.TLSR)


  def analitic(self, symbol:str, timeframe:str):
    """



    """
    steps = 30000
    count = int (0)
    while count <= steps:
      count += 1
      


      df3m = self.exchange.GetSymbolKlines(symbol = symbol, interval = "3m", limit = 140)
      df3m = self.technicalAnalsis(df3m)
      dfSlope3m = self.slopCalculator(df3m)


      df5m = self.exchange.GetSymbolKlines(symbol = symbol, interval = "5m", limit = 140)
      df5m = self.technicalAnalsis(df5m)
      dfSlope5m = self.slopCalculator(df5m)



      df15m = self.exchange.GetSymbolKlines(symbol = symbol, interval = "15m", limit = 140)
      df15m = self.technicalAnalsis(df15m)
      dfSlope15m = self.slopCalculator(df15m)



      strategy_result3m = Strategies.tlStrategyLiveLong(df = df3m, dfSlope=dfSlope3m, step = len(df3m['close'])-1)
      strategy_result3mprev = Strategies.tlStrategyLiveLong(df = df3m, dfSlope=dfSlope3m, step = len(df3m['close'])-2)


      strategy_result5m = Strategies.tlStrategyLiveLong(df = df5m, dfSlope=dfSlope5m, step = len(df5m['close'])-1)
      strategy_result5mprev = Strategies.tlStrategyLiveLong(df = df5m, dfSlope=dfSlope5m, step = len(df5m['close'])-2)


      strategy_result15m = Strategies.tlStrategyLiveLong(df = df15m, dfSlope=dfSlope15m, step = len(df15m['close'])-1)
      strategy_result15mprev = Strategies.tlStrategyLiveLong(df = df15m, dfSlope=dfSlope15m, step = len(df15m['close'])-2)
      
      current_time = datetime.datetime.now()
      print("\n\n                   Current Time: \033[1;36;40m"+ str(current_time)+"\033[m")
      print("Parameter                  3m                  5m                  15m")
      print("indicator                  "+str(strategy_result3m)+"                  "+str(strategy_result5m)+"                  "+str(strategy_result15m))
      print("indicatorPre               "+str(strategy_result3mprev)+"                  "+str(strategy_result5mprev)+"                  "+str(strategy_result15mprev))
      print("                 "+str(self.indicatorMap[strategy_result3m])+"    "+
            str(self.indicatorMap[strategy_result5m])+"    "+
            str(self.indicatorMap[strategy_result15m]))

      time.sleep(60)

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
  ts.sign("BTCUSDT", "1m")
  #ts.analitic("BTCUSDT", "5m")


if __name__ == '__main__':
  Main()

