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
    self.TLSR = []
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


    self.tFrameUp = {"1m" : "3m",
                     "3m" : "5m",
                     "5m" : "15m",
                    "15m" : "30m",
                    "30m" : "1h",
                     "1h" : "4h",
                     "2h" : "4h",
                     "4h" : "1D"}



  def backtesting(self, symbol:str, timeframe:str):
    """

    """

    df = self.exchange.GetSymbolKlines(symbol = symbol, interval = timeframe, limit = 20000)

    backTestStrategy = Strategies()
    df = backTestStrategy.SslEMA(df)
    print(df)
    dataTrade = {
            'initialBalance': 100.0,
            'finalBalance'  : 100.0,
            'entryPrice'    : 00.0,
            'percent'       : 00.0,
            'dateEntry'     : '',
            'closePrice'    : 00.0,
            'dateClose'     : '',
            'totalTrades'   : 0,
            'signalE':'',
            'signalC':'',
    }
    backtestDf = pd.DataFrame(columns=['initialBalance',
                                       'finalBalance',
                                       'entryPrice',
                                       'percent',
                                       'dateEntry',
                                       'closePrice',
                                       'dateClose',
                                       'totalTrades',
                                       'signalE',
                                       'signalC',])

    entryLong = 'off'
    for i in range(0, len(df['close'])):
      if df['signal'][i] == 'long' and entryLong == 'off':
        entryLong = 'on'
        dataTrade['entryPrice'] = df['close'][i]
        dataTrade['dateEntry'] = df['date'][i]
        dataTrade['totalTrades'] += 1
        dataTrade['signalE'] = df['signal'][i]
        backtestDf = backtestDf.append(dataTrade, ignore_index=True, sort=False)
      elif df['signal'][i] == 'closeLong' and entryLong == 'on':
        entryLong = 'off'
        #dataTrade['closePrice'] = df['close'][i]
        #dataTrade['dateClose'] = df['date'][i]
        percent = ((df['close'][i]/dataTrade['entryPrice']) * 100) - 100
        dataTrade['finalBalance'] += (dataTrade['finalBalance'] * percent) / 100
        

        backtestDf["closePrice"].iloc[-1]   = df['close'][i]
        backtestDf["dateClose"].iloc[-1]    = df['date'][i]
        backtestDf["percent"].iloc[-1]      = percent 
        backtestDf['finalBalance'].iloc[-1] = dataTrade['finalBalance']
        backtestDf['signalC'].iloc[-1]      = df['signal'][i]
        #backtestDf = backtestDf.append(dataTrade, ignore_index=True, sort=False)

    print("\n  **  Data  **")
    print('Symbol: ' + symbol)
    print('Time Frame: ' + timeframe)
    print('\n')
    print(backtestDf)
    backtestDf.to_csv("backtestDf.csv", sep='\t')



  def sign(self, symbol:str, timeframe:str):
    """

    """

    df = self.exchange.GetSymbolKlines(symbol = symbol, interval = timeframe, limit = 20000)

    SqueezMIndicator = Strategies()
    strategy_result = SqueezMIndicator.SqueezMIndicator(df)
    df = strategy_result[0]
    listResult = strategy_result[1]



    print(df)
    print(listResult)

 

    for i in range(0, len(df['close'])):
      self.TLSR.append([df['date'][i], df['signal'][i], df['high'][i], df['low'][i]])

    #for i in range(0, len(df['close'])):
    #  print(str(df.loc[i,'date'])+"\t"+str(df.loc[i,'signal'])+"\t"+str(dfSlope.loc[i,'histSlope'])+"\t"+str(dfSlope.loc[i,'adxSlope'])+"\t"+str(dfSlope.loc[i,'adxStatus'])+"\t"+str(df.loc[i,'ADX']))

    df.to_csv("df.csv", sep='\t')
    

    self.chart.plotData(df, symbol, timeframe, self.param, self.TLSR)

"""
  def analitic(self, symbol:str, timeframe:str):

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
"""


def Main():

  ts = tradeSigns()
  ts.sign("BTCUSDT", "30m")
  #ts.analitic("BTCUSDT", "5m")


if __name__ == '__main__':
  Main()

