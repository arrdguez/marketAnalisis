#!/usr/bin/python3

import pandas as pd
from finta import TA

import time
import datetime
from datetime import date
import sys
sys.path.insert(1, '../')
from exchange.binance import Binance
from strategies.strategies import Strategies
from plot.plot import chart
#import exchange
import pprint
import math

import glob                                         #to get the name of multiple files 
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



  def backtesting(self, symbol:str, 
                     timeframe:str, 
                          smaL:int = 8, 
                     emalength:int = 200,
                           btd:bool = True,
             printAllDataFrame: bool = True,
                       restart:bool = True, 
                         limit:int = 1000,
                      position:str = 'short',
                      strategy:str = None,
                      fromFile:str = False,
                         param:dict = {}):
    """
      position : long/short/both/
    """
    if strategy == None:
      print('You should provide a strategy to test.')
      #exit()
    else:
      print('The strategy '+strategy+' will be test with the next specification:')
    
    if fromFile:
      print('The data is obtain from local directory.')
      list_of_files = glob.glob('/home/rfeynman/Dropbox/src/BinanceDB/*.csv')
      df = pd.DataFrame()  

      for x in list_of_files:
        tmpString = x[list_of_files[0].find('_')-9:]
        if tmpString[tmpString.find('_')+1:tmpString.find('.')] == timeframe and tmpString[tmpString.find('/')+1:tmpString.find('_')] == symbol:
          print(tmpString[tmpString.find('_')+1:tmpString.find('.')])
          print(tmpString[tmpString.find('/')+1:tmpString.find('_')])
          df = pd.read_csv(x, sep = '\t')
          df['date'] = pd.to_datetime(df['date'])
 
          #print(df)
          #exit()
         
    else:
      print('The data will by obtain from Binance')
      df = self.exchange.GetSymbolKlines(symbol = symbol, interval = timeframe, limit = limit)
    backTestStrategy = Strategies()

    df = backTestStrategy.SslEMA(df, emalength = emalength, smalength = smaL)
    
    print('  **  Back-testing in progress  ** ')
    
    if position == 'long':
      result = self.long(df = df, symbol = symbol, timeframe = timeframe, restart = restart)
      df = result[0]
      resume = result[1]
      backtestDetail = result[2]
      temporalDict = result[3]
      print(result[2])    
    elif position == 'short':
      result = self.short(df = df, symbol = symbol, timeframe = timeframe, restart = restart)
      df = result[0]
      resume = result[1]
      backtestDetail = result[2]
      temporalDict = result[3]
      print(result[2])    
    exit()


    df['trade'] = ''
    dataTrade = {'initialBalance': 100.0,
                 'finalBalance'  : 100.0,
                 'entryPrice'    : 00.0,
                 'dateEntry'     : '',
                 'closePrice'    : 00.0,
                 'dateClose'     : '',
                 'signalE':'',
                 'signalC':'',}

    resume = {'symbol'         : '',  # before loop
              'timeframe'      : '',  # before loop
              'backTestPeriod' : '',  # before loop
              'totalProfit'    : 0,   # end loop
              'totalTrades'    : 0,   # each long&short cycle
              'initialBalance' : 0,   # end loop
              'finalBalance'   : 0,   # end loop
              'longN'          : 0,    # each cycle
              'longProfit'     : 0,    # each cycle
              'longMaxP'       : 0,    # end loop
              'longMinP'       : 0,    # end loop
              'longMaxPeriod'  : 0,    # end loop
              'longMinPeriod'  : 0,    # end loop
              'longCloseBySL'  : 0,    # each cycle

              'shortN'         : 0,   # each cycle
              'shortProfit'    : 0,   # each cycle
              'shortMaxP'      : 0,   # end loop
              'shortMinP'      : 0,   # end loop
              'shortMaxPeriod' : 0,   # end loop
              'shortMinPeriod' : 0,   # end loop
              'shortCloseBySL' : 0}   # each cycle



    backtestDetail = pd.DataFrame(columns = ['totalTrades',    #entry all
                                             'initialBalance', #before loop
                                             'finalBalance',   #close all
                                             'entryPrice',     #entry all
                                             'closePrice',     #close all
                                             'percent',        #close all
                                             'dateEntry',      #entry all
                                             'dateClose',      #close all
                                             'long',           #entry long
                                             'short',          #entry long
                                             'stopLoss',       #close all
                                             'signalEntry',    #entry all
                                             'signalClose',    #close all
                                             'profit',
                                             'period'])        #close all


    temporalDict = {'totalTrades' : '',
                    'initialBalance' : '',
                    'finalBalance' : '',
                    'entryPrice' : '',
                    'closePrice' : '',
                    'percent' : '',
                    'dateEntry' : '',
                    'dateClose' : '',
                    'long' : '',
                    'short' : '',
                    'stopLoss' : '',
                    'signalEntry' : '',
                    'signalClose' : '',
                    'period' : ''}

    

    #BackTesting Loop
    resume['symbol'] = symbol
    resume['timeframe'] = timeframe
    resume['backTestPeriod'] = (df['date'].iloc[-1]) - (df['date'].iloc[0])
    resume['backTestPeriod'] = str((resume['backTestPeriod'].seconds/60)/24)+' days'
    backtestDetail['initialBalance'] = 100
    entryLong = 'off'
    entryShort = 'off'

    for i in range(0, len(df['close'])):

      #if entryLong == 'off' and entryShort == 'off' and df['trade'][i - 1] == 1:
      #  df['trade'].iloc[i] = '2'

      #"""
      #Take long position
      if df['LongSignals'][i] == 'long' and entryLong == 'off' and entryShort == 'off':

        entryLong = 'on'
        dataTrade['entryPrice'] = df['close'][i]
        dataTrade['dateEntry'] = df['date'][i]
        dataTrade['signalE'] = df['LongSignals'][i]
        resume['totalTrades'] += 1
        resume['longN'] += 1
        temporalDict['totalTrades']  = resume['totalTrades']
        temporalDict['entryPrice']   = dataTrade['entryPrice']
        temporalDict['dateEntry']    = dataTrade['dateEntry']
        temporalDict['long']         = True
        temporalDict['short']        = False
        temporalDict['signalEntry']  = df['LongSignals'][i]
        backtestDetail = backtestDetail.append(temporalDict, ignore_index=True, sort=False)
        df['trade'].iloc[i] = 'openLong'

      #Close long position
      elif df['LongSignals'].iloc[i] == 'closeLong' and entryLong == 'on':

        entryLong = 'off'
        percent   = ((df['close'].iloc[i]/dataTrade['entryPrice']) * 100) - 100

        if restart:
          profit = (dataTrade['initialBalance'] * percent) / 100
        else:
          profit = (dataTrade['finalBalance'] * percent) / 100

        dataTrade['finalBalance'] += profit
        dataTrade['closePrice']   = df['close'][i]
        dataTrade['dateClose']    = df['date'][i]
        dataTrade['signalC']      = df['LongSignals'][i]

        resume['longProfit'] += profit

        #backtestDetail['finalBalance'].iloc[-1] = tradeSigns.truncate(dataTrade['finalBalance'], 2)
        backtestDetail.loc[-1, ('finalBalance')] = tradeSigns.truncate(dataTrade['finalBalance'], 2)
        #backtestDetail["closePrice"].iloc[-1]   = df['close'][i]
        backtestDetail.loc[-1, ("closePrice")]   = df['close'][i]
        #backtestDetail["percent"].iloc[-1]      = tradeSigns.truncate(percent, 2)
        backtestDetail.loc[-1, ("percent")]      = tradeSigns.truncate(percent, 2)
        #backtestDetail["dateClose"].iloc[-1]    = df['date'][i]
        backtestDetail.loc[-1, ("dateClose")]    = df['date'][i]
        #backtestDetail['stopLoss'].iloc[-1]     = False
        backtestDetail.loc[-1, ('stopLoss')]     = False
        #backtestDetail['profit'].iloc[-1]       = tradeSigns.truncate(profit, 2)
        backtestDetail.loc[-1, ('profit')]       = tradeSigns.truncate(profit, 2)

        if (backtestDetail['dateClose'].iloc[-1] - backtestDetail['dateEntry'].iloc[-1]).days == 0:
          #backtestDetail['period'].iloc[-1]       = (backtestDetail['dateClose'].iloc[-1] - backtestDetail['dateEntry'].iloc[-1]).seconds/60
          backtestDetail.loc[-1, ('period')]       = (backtestDetail['dateClose'].iloc[-1] - backtestDetail['dateEntry'].iloc[-1]).seconds/60
        else:
          #backtestDetail['period'].iloc[-1]       = (backtestDetail['dateClose'].iloc[-1] - backtestDetail['dateEntry'].iloc[-1]).days
          backtestDetail.loc[-1, ('period')]       = (backtestDetail['dateClose'].iloc[-1] - backtestDetail['dateEntry'].iloc[-1]).days
        #backtestDetail['signalClose'].iloc[-1]  = df['LongSignals'][i]
        backtestDetail.loc[-1, ('signalClose')]  = df['LongSignals'][i]
        

        #df['trade'].iloc[i] = 'closeLong'
        df.loc[i, ('trade')] = 'closeLong'


      #Close long position by stop loss
      elif df['LongSignals'].iloc[i] == 'closeLongSL' and entryLong == 'on':
        
        entryLong = 'off'
        percent   = ((df.loc[i, ('close')]/dataTrade['entryPrice']) * 100) - 100
        if restart:
          profit = (dataTrade['initialBalance'] * percent) / 100
        else:
          profit = (dataTrade['finalBalance'] * percent) / 100

        dataTrade['finalBalance'] += profit
        dataTrade['finalBalance'] += profit
        dataTrade['closePrice']   = df['close'][i]
        dataTrade['dateClose']    = df['date'][i]
        dataTrade['signalC']      = df['LongSignals'][i]

        
        resume['longCloseBySL'] += 1
        resume['longProfit'] += profit

        #backtestDetail['finalBalance'].iloc[-1] = tradeSigns.truncate(dataTrade['finalBalance'], 2)
        backtestDetail['finalBalance'].iloc[-1] = tradeSigns.truncate(dataTrade['finalBalance'], 2)
        #backtestDetail["closePrice"].iloc[-1]   = df['close'][i]
        backtestDetail.loc[-1, ("closePrice")]   = df['close'][i]
        #backtestDetail["percent"].iloc[-1]      = tradeSigns.truncate(percent, 2)
        backtestDetail.loc[-1, ("percent")]      = tradeSigns.truncate(percent, 2)
        #backtestDetail["dateClose"].iloc[-1]    = df['date'][i]
        backtestDetail.loc[-1, ("dateClose")]    = df['date'][i]
        #backtestDetail['stopLoss'].iloc[-1]     = True
        backtestDetail.loc[-1, ('stopLoss')]     = True
        #backtestDetail['profit'].iloc[-1]       = tradeSigns.truncate(profit, 2)
        backtestDetail.loc[-1, ('profit')]       = tradeSigns.truncate(profit, 2)
        #backtestDetail['period'].iloc[-1]       = backtestDetail['dateClose'].iloc[-1] - backtestDetail['dateEntry'].iloc[-1]
        backtestDetail.loc[-1, ('period')]       = backtestDetail['dateClose'].iloc[-1] - backtestDetail['dateEntry'].iloc[-1]
        #backtestDetail['signalClose'].iloc[-1]  = df['LongSignals'][i]
        backtestDetail.loc[-1, ('signalClose')]  = df['LongSignals'][i]

        if (backtestDetail['dateClose'].iloc[-1] - backtestDetail['dateEntry'].iloc[-1]).days == 0:
          #backtestDetail['period'].iloc[-1]       = (backtestDetail['dateClose'].iloc[-1] - backtestDetail['dateEntry'].iloc[-1]).seconds/60
          backtestDetail.loc[-1, ('period')]       = (backtestDetail['dateClose'].iloc[-1] - backtestDetail['dateEntry'].iloc[-1]).seconds/60
        else:
          #backtestDetail['period'].iloc[-1]       = (backtestDetail['dateClose'].iloc[-1] - backtestDetail['dateEntry'].iloc[-1]).days
          backtestDetail.loc[-1, ('period')]       = (backtestDetail['dateClose'].iloc[-1] - backtestDetail['dateEntry'].iloc[-1]).days
        #backtestDetail['signalClose'].iloc[-1]  = df['LongSignals'][i]
        backtestDetail.loc[-1, ('signalClose')]  = df['LongSignals'][i]

        #df['trade'].iloc[i] = 'c'
        df.loc[i, ('trade')] = 'closeLongBySL'

      #Take short position
      if df['ShortSignals'][i] == 'short' and entryLong == 'off' and entryShort == 'off':
        
        entryShort = 'on'
        dataTrade['entryPrice'] = df['close'][i]
        dataTrade['dateEntry'] = df['date'][i]
        dataTrade['signalE'] = df['ShortSignals'][i]

        resume['totalTrades'] += 1
        resume['shortN'] += 1

        temporalDict['totalTrades']  = resume['totalTrades']
        temporalDict['entryPrice']   = dataTrade['entryPrice']
        temporalDict['dateEntry']    = dataTrade['dateEntry']
        temporalDict['long']         = False
        temporalDict['short']        = True
        temporalDict['signalEntry']  = df['ShortSignals'][i]
        
        backtestDetail = backtestDetail.append(temporalDict, ignore_index=True, sort=False)

        #df['trade'].iloc[i] = 'd'
        df.loc[i, ('trade')] = 'openShort'

      #Close short position
      elif df['ShortSignals'].iloc[i] == 'closeShort' and entryShort == 'on':
        
        entryShort = 'off'
        percent   = -1 * (((df['close'].iloc[i]/dataTrade['entryPrice']) * 100) - 100)

        if restart:
          profit = (dataTrade['initialBalance'] * percent) / 100
        else:
          profit = (dataTrade['finalBalance'] * percent) / 100

        dataTrade['finalBalance'] += profit
        dataTrade['closePrice']   = df['close'][i]
        dataTrade['dateClose']    = df['date'][i]
        dataTrade['signalC']      = df['ShortSignals'][i]
        
        resume['shortProfit'] += profit

        #backtestDetail['finalBalance'].iloc[-1] = tradeSigns.truncate(dataTrade['finalBalance'], 2)
        backtestDetail.loc[-1, ('finalBalance')] = tradeSigns.truncate(dataTrade['finalBalance'], 2)
        #backtestDetail["closePrice"].iloc[-1]   = df['close'][i]
        backtestDetail.loc[-1, ("closePrice")]   = df['close'][i]
        #backtestDetail["percent"].iloc[-1]      = tradeSigns.truncate(percent, 2)
        backtestDetail.loc[-1, ("percent")]      = tradeSigns.truncate(percent, 2)
        #backtestDetail["dateClose"].iloc[-1]    = df['date'][i]
        backtestDetail.loc[-1, ("dateClose")]    = df['date'][i]
        #backtestDetail['stopLoss'].iloc[-1]     = False
        backtestDetail.loc[-1, ('stopLoss')]     = False
        #backtestDetail['profit'].iloc[-1]       = tradeSigns.truncate(profit, 2)
        backtestDetail.loc[-1, ('profit')]       = tradeSigns.truncate(profit, 2)

        if (backtestDetail['dateClose'].iloc[-1] - backtestDetail['dateEntry'].iloc[-1]).days <= 0:
          #backtestDetail['period'].iloc[-1]       = (backtestDetail['dateClose'].iloc[-1] - backtestDetail['dateEntry'].iloc[-1]).seconds/60
          backtestDetail.loc[-1, ('period')]       = (backtestDetail['dateClose'].iloc[-1] - backtestDetail['dateEntry'].iloc[-1]).seconds/60
        else:
          #backtestDetail['period'].iloc[-1]       = (backtestDetail['dateClose'].iloc[-1] - backtestDetail['dateEntry'].iloc[-1]).days
          backtestDetail.loc[-1, ('period')]       = (backtestDetail['dateClose'].iloc[-1] - backtestDetail['dateEntry'].iloc[-1]).days
        #backtestDetail['signalClose'].iloc[-1]  = df['ShortSignals'][i]
        backtestDetail.loc[-1, ('signalClose')]  = df['ShortSignals'][i]

        #df['trade'].iloc[i] = 'e'
        df.loc[i, ('trade')] = 'closeShort'


      #Close long position by stop loss
      elif df['ShortSignals'].iloc[i] == 'closeShortSL' and entryShort == 'on':
        
        entryShort = 'off'

        percent = -1 * (((df['close'].iloc[i]/dataTrade['entryPrice']) * 100) - 100)
        percent = tradeSigns.truncate(percent, 3)
        if restart:
          profit = tradeSigns.truncate((dataTrade['initialBalance'] * percent) / 100, 3)
        else:
          profit = tradeSigns.truncate((dataTrade['finalBalance'] * percent) / 100, 3)
        dataTrade['finalBalance'] += profit
        dataTrade['finalBalance'] += profit
        dataTrade['closePrice']   = df['close'][i]
        dataTrade['dateClose']    = df['date'][i]
        dataTrade['signalC']      = df['ShortSignals'][i]

        resume['shortCloseBySL'] += 1
        resume['shortProfit'] += profit

        #backtestDetail['finalBalance'].iloc[-1] = tradeSigns.truncate(dataTrade['finalBalance'], 2)
        backtestDetail.loc[-1, ('finalBalance')] = tradeSigns.truncate(dataTrade['finalBalance'], 2)
        #backtestDetail["closePrice"].iloc[-1]   = df['close'][i]
        backtestDetail.loc[-1, ("closePrice")]   = df['close'][i]
        #backtestDetail["percent"].iloc[-1]      = tradeSigns.truncate(percent, 2)
        backtestDetail.loc[-1, ("percent")]      = tradeSigns.truncate(percent, 2)
        #backtestDetail["dateClose"].iloc[-1]    = df['date'][i]
        backtestDetail.loc[-1, ("dateClose")]    = df['date'][i]
        #backtestDetail['stopLoss'].iloc[-1]     = True
        backtestDetail.loc[-1, ('stopLoss')]     = True
        #backtestDetail['period'].iloc[-1]       = backtestDetail['dateClose'].iloc[-1] - backtestDetail['dateEntry'].iloc[-1]
        backtestDetail.loc[-1, ('period')]       = backtestDetail['dateClose'].iloc[-1] - backtestDetail['dateEntry'].iloc[-1]
        #backtestDetail['signalClose'].iloc[-1]  = df['ShortSignals'][i]
        backtestDetail.loc[-1, ('signalClose')]  = df['ShortSignals'][i]
        #backtestDetail['profit'].iloc[-1]       = tradeSigns.truncate(profit, 2)
        backtestDetail.loc[-1, ('profit')]       = tradeSigns.truncate(profit, 2)

        if (backtestDetail['dateClose'].iloc[-1] - backtestDetail['dateEntry'].iloc[-1]).days <= 0:
          #backtestDetail['period'].iloc[-1]       = (backtestDetail['dateClose'].iloc[-1] - backtestDetail['dateEntry'].iloc[-1]).seconds/60
          backtestDetail.loc[-1, ('period')]       = (backtestDetail['dateClose'].iloc[-1] - backtestDetail['dateEntry'].iloc[-1]).seconds/60
        else:
          #backtestDetail['period'].iloc[-1]       = (backtestDetail['dateClose'].iloc[-1] - backtestDetail['dateEntry'].iloc[-1]).days
          backtestDetail.loc[-1, ('period')]       = (backtestDetail['dateClose'].iloc[-1] - backtestDetail['dateEntry'].iloc[-1]).days
        #backtestDetail['signalClose'].iloc[-1]  = df['ShortSignals'][i]
        backtestDetail.loc[-1, ('signalClose')]  = df['ShortSignals'][i]

        #df['trade'].iloc[i] = 'f'
        df.loc[i, ('trade')] = 'closeShortBySL'
        
    #long
    try:
      resume['longMaxP'] = max(list(backtestDetail[backtestDetail.long == True]['percent']))
    except:
      resume['longMaxP'] = 0
    try:
      resume['longMinP'] = min(list(backtestDetail[backtestDetail.long == True]['percent']))
    except:
      resume['longMinP'] = 0

    #short
    try:
      resume['shortMaxP'] = max(list(backtestDetail[backtestDetail.short == True]['percent']))
    except:
      resume['shortMaxP'] = 0
    try:
      resume['shortMinP'] = min(list(backtestDetail[backtestDetail.short == True]['percent']))
    except:
      resume['shortMinP'] = 0 

    resume['totalProfit'] = backtestDetail['profit'].sum()
    resume['initialBalance'] = dataTrade['initialBalance']
    resume['finalBalance'] = dataTrade['finalBalance']
    

    #try:
    #  resume['finalBalance'] = backtestDetail['finalBalance'][-1]
    #except:
    #  resume['finalBalance'] = backtestDetail['finalBalance'][-2]


    #print(backtestDetail)
    #print('\n')
    #pprint.pprint(resume)


    #change the name of this variable btd = print back test details
    if btd:
      filename = './BTResults/BackTestDetail_'+symbol+'_'+str(timeframe)+'.resume'
      
      with open(filename, 'w') as f:
        f.write('#Details of the back test of the strategy.')
        f.write('\n#NOTE.1: All notes are write using \'#\' to by consider like comments in case you want to pass this file to gnuplot for example.')
        f.write('\n#NOTE.2: I am working on  duration period, due to it is not clear if is in minutes or seconds')
        f.write('\n')
        f.write('\n')
        f.write('\n#-------------- RESUME --------------')
        f.write('\n#               DATE')
        f.write('\n#SYMBOL:            ' + resume['symbol'])
        f.write('\n#TIMEFRAME:         ' + resume['timeframe'])
        f.write('\n#BACK Test PERIODO: ' + str(resume['backTestPeriod']))
        f.write('\n#FINAL BALANCE:     ' + str(dataTrade['finalBalance']))
        f.write('\n')
        f.write('\n#TOTAL PROFIT:      ' + str(resume['totalProfit']))
        f.write('\n#TOTAL TRADES:      ' + str(resume['totalTrades']))
        f.write('\n')
        f.write('\n#-------------- LONG ----------------')
        f.write('\n#TOTAL LONG:        ' + str(resume['longN']))
        f.write('\n#LONG CLOSED BY SL: ' + str(resume['longCloseBySL']))
        f.write('\n#LONG PROFIT:       ' + str(resume['longProfit']))
        f.write('\n#MAX LONG PROFIT:   ' + str(resume['longMaxP']))
        f.write('\n#MIN LONG PROFIT:   ' + str(resume['longMinP']))
        f.write('\n#MAX DURATION LONG: ' + str(resume['longMaxPeriod']))
        f.write('\n#MIN DURATION LONG: ' + str(resume['longMinPeriod']))
        f.write('\n')
        f.write('\n#-------------- SHORT ----------------')
        f.write('\n#TOTAL SHORT:        ' + str(resume['shortN']))
        f.write('\n#SHORT CLOSED BY SL: ' + str(resume['shortCloseBySL']))
        f.write('\n#SHORT PROFIT:       ' + str(resume['shortProfit']))
        f.write('\n#MAX SHORT PROFIT:   ' + str(resume['shortMaxP']))
        f.write('\n#MIN SHORT PROFIT:   ' + str(resume['shortMinP']))
        f.write('\n#MAX DURATION SHORT: ' + str(resume['shortMaxPeriod']))
        f.write('\n#MIN DURATION SHORT: ' + str(resume['shortMinPeriod']))
        f.write('\n')
        f.write('\n')
        f.write('\n#--------- STRATEGY PARAMETERS -------')
        f.write('\n#SMA:            '+ str(smaL))
        f.write('\n#EMA:            '+ str(emalength))
        f.write('\n#LENGTH OF DATA: '+ str(limit))
        f.write('\n#RESTART:        '+ str(restart))
        f.write('\n')
        f.write('\n#DATA FRAME')
        f.write('\n')
        f.write('\n')

      pfile = open(filename, 'a')
      pfile.write(backtestDetail.to_string())
      pfile.close()

      if printAllDataFrame: 
        with open(filename, 'a') as f:
          f.write('\n\n**   FULL DATA ***\n')

      pfile = open(filename, 'a')
      pfile.write(df.to_string())
      pfile.close()
      
      #backtestDetail.to_csv(filename, sep='\t')


    self.chart.plotEachTrade(df = df, symbol = symbol, timeframe = timeframe)
    return resume



  def BacktestLoop(self):
              

    

    symbol = ['ADAUSDT','BTCUSDT','ETHUSDT','BNBUSDT', 'XRPUSDT', "LTCUSDT", 'AVAXUSDT']
    timeframe = ['1m', '3m', '5m', '15m', '30m', '1h', '4h']
    
    '''
    for i in symbol:
      for x in timeframe:
        filename = str(i)+'_'+str(x)+'.csv'
        print(i)
        df = self.exchange.GetSymbolKlines(symbol = i, interval = x, limit = 20000)
        df.to_csv(filename, sep = '\t', index = False, columns = ['open','high', 'low', 'close', 'volume', 'date',])
        #pfile = open(filename, 'w')
        #pfile.write(df.to_string())
        #pfile.close()
    
    exit()
    '''

    BackTestResume = pd.DataFrame(columns = ['symbol',
                                             'timeframe',
                                             'backTestPeriod',
                                             'totalProfit',
                                             'totalTrades',
                                             'initialBalance',
                                             'finalBalance',
                                             'longN',
                                             'longProfit',
                                             'longMaxP',
                                             'longMinP',
                                             'longMaxPeriod',
                                             'longMinPeriod',
                                             'longCloseBySL',
                                             'shortN',
                                             'shortProfit',
                                             'shortMaxP',
                                             'shortMinP',
                                             'shortMaxPeriod',
                                             'shortMinPeriod',
                                             'shortCloseBySL',])

    symbol = ['BTCUSDT']
    timeframe = ['1m']
    smaL = [10]
    


    #timeframe = ['15m']
    #smaL = [8]
    
    for i in range(len(symbol)):
      for x in range(len(timeframe)):
        for y in range(len(smaL)):
          print(symbol[i])
          print(timeframe[x])
          result = self.backtesting(symbol[i], timeframe[x], smaL[y], restart = False, limit = 500, fromFile = False, emalength = 200,)
          #pprint.pprint(result)
          BackTestResume = BackTestResume.append(result, ignore_index=True, sort=False)
          #print(BackTestResume)
    
    #change the name of this variable btd = print back test details
    
    filename = './BTResults/BackTestDetail.dat'
    with open(filename, 'w') as f:
      f.write('#Result of the back testing for some symbols, timeframes, parameters.')
      f.write('\n')
      f.write('\n')
    

    
    pfile = open(filename, 'a')
    pfile.write(BackTestResume.to_string())
    pfile.close()
 

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


  def short(self, df, symbol, timeframe, restart:bool = True):
    print('  **  Running short  **')
    
    df['trade'] = ''
    dataTrade = {'initialBalance': 100.0,
                   'finalBalance'  : 100.0,
                   'entryPrice'    : 00.0,
                   'dateEntry'     : '',
                   'closePrice'    : 00.0,
                   'dateClose'     : '',
                   'signalE':'',
                   'signalC':'',}

    resume = {'symbol'           : '',  # before loop
                'timeframe'      : '',  # before loop
                'backTestPeriod' : '',  # before loop
                'totalProfit'    : 0,   # end loop
                'totalTrades'    : 0,   # each long&short cycle
                'initialBalance' : 0,   # end loop
                'finalBalance'   : 0,   # end loop
                'longN'          : 0,    # each cycle
                'longProfit'     : 0,    # each cycle
                'longMaxP'       : 0,    # end loop
                'longMinP'       : 0,    # end loop
                'longMaxPeriod'  : 0,    # end loop
                'longMinPeriod'  : 0,    # end loop
                'longCloseBySL'  : 0,    # each cycle
                'shortN'         : 0,   # each cycle
                'shortProfit'    : 0,   # each cycle
                'shortMaxP'      : 0,   # end loop
                'shortMinP'      : 0,   # end loop
                'shortMaxPeriod' : 0,   # end loop
                'shortMinPeriod' : 0,   # end loop
                'shortCloseBySL' : 0}   # each cycle

    backtestDetail = pd.DataFrame(columns = [  'totalTrades',    #entry all
                                               'initialBalance', #before loop
                                               'finalBalance',   #close all
                                               'entryPrice',     #entry all
                                               'closePrice',     #close all
                                               'percent',        #close all
                                               'dateEntry',      #entry all
                                               'dateClose',      #close all
                                               'long',           #entry long
                                               'short',          #entry long
                                               'stopLoss',       #close all
                                               'signalEntry',    #entry all
                                               'signalClose',    #close all
                                               'profit',
                                               'period'])        #close all

    temporalDict = {  'totalTrades' : '',
                      'initialBalance' : '',
                      'finalBalance' : '',
                      'entryPrice' : '',
                      'closePrice' : '',
                      'percent' : '',
                      'dateEntry' : '',
                      'dateClose' : '',
                      'long' : '',
                      'short' : '',
                      'stopLoss' : '',
                      'signalEntry' : '',
                      'signalClose' : '',
                      'period' : ''}

    #BackTesting Loop
    resume['symbol'] = symbol
    resume['timeframe'] = timeframe
    resume['backTestPeriod'] = (df['date'].iloc[-1]) - (df['date'].iloc[0])
    resume['backTestPeriod'] = str((resume['backTestPeriod'].seconds/60)/24)+' days'
    backtestDetail['initialBalance'] = 100
    entryLong = 'off'
    entryShort = 'off'
  
    


    return df,resume, backtestDetail, temporalDict

  def long(self, df, symbol, timeframe, restart:bool = True):
    print('  **  Running long  **')
    
    df['trade'] = ''
    dataTrade = {'initialBalance': 100.0,
                   'finalBalance'  : 100.0,
                   'entryPrice'    : 00.0,
                   'dateEntry'     : '',
                   'closePrice'    : 00.0,
                   'dateClose'     : '',
                   'signalE':'',
                   'signalC':'',}

    resume = {'symbol'           : '',  # before loop
                'timeframe'      : '',  # before loop
                'backTestPeriod' : '',  # before loop
                'totalProfit'    : 0,   # end loop
                'totalTrades'    : 0,   # each long&short cycle
                'initialBalance' : 0,   # end loop
                'finalBalance'   : 0,   # end loop
                'longN'          : 0,    # each cycle
                'longProfit'     : 0,    # each cycle
                'longMaxP'       : 0,    # end loop
                'longMinP'       : 0,    # end loop
                'longMaxPeriod'  : 0,    # end loop
                'longMinPeriod'  : 0,    # end loop
                'longCloseBySL'  : 0,    # each cycle
                'shortN'         : 0,   # each cycle
                'shortProfit'    : 0,   # each cycle
                'shortMaxP'      : 0,   # end loop
                'shortMinP'      : 0,   # end loop
                'shortMaxPeriod' : 0,   # end loop
                'shortMinPeriod' : 0,   # end loop
                'shortCloseBySL' : 0}   # each cycle

    backtestDetail = pd.DataFrame(columns = [  'totalTrades',    #entry all
                                               'initialBalance', #before loop
                                               'finalBalance',   #close all
                                               'entryPrice',     #entry all
                                               'closePrice',     #close all
                                               'percent',        #close all
                                               'dateEntry',      #entry all
                                               'dateClose',      #close all
                                               'long',           #entry long
                                               'short',          #entry long
                                               'stopLoss',       #close all
                                               'signalEntry',    #entry all
                                               'signalClose',    #close all
                                               'profit',
                                               'period'])        #close all

    temporalDict = {  'totalTrades' : '',
                      'initialBalance' : '',
                      'finalBalance' : '',
                      'entryPrice' : '',
                      'closePrice' : '',
                      'percent' : '',
                      'dateEntry' : '',
                      'dateClose' : '',
                      'long' : '',
                      'short' : '',
                      'stopLoss' : '',
                      'signalEntry' : '',
                      'signalClose' : '',
                      'period' : ''}

    #BackTesting Loop
    resume['symbol'] = symbol
    resume['timeframe'] = timeframe
    resume['backTestPeriod'] = (df['date'].iloc[-1]) - (df['date'].iloc[0])
    resume['backTestPeriod'] = str((resume['backTestPeriod'].seconds/60)/24)+' days'
    backtestDetail['initialBalance'] = 100
    entryLong = 'off'
    entryShort = 'off'


    for i in range(0, len(df['close'])):


      #Take long position
      if df['LongSignals'][i] == 'long' and entryLong == 'off' and entryShort == 'off':

        entryLong = 'on'
        dataTrade['entryPrice'] = df['close'][i]
        dataTrade['dateEntry'] = df['date'][i]
        dataTrade['signalE'] = df['LongSignals'][i]
        resume['totalTrades'] += 1
        resume['longN'] += 1
        temporalDict['totalTrades']  = resume['totalTrades']
        temporalDict['entryPrice']   = dataTrade['entryPrice']
        temporalDict['dateEntry']    = dataTrade['dateEntry']
        temporalDict['long']         = True
        temporalDict['short']        = False
        temporalDict['signalEntry']  = df['LongSignals'][i]
        backtestDetail = backtestDetail.append(temporalDict, ignore_index=True, sort=False)
        #df['trade'].iloc[i] = 'openLong'
        df.loc[i, ('trade')] = 'openLong'

      #Close long position
      elif df['LongSignals'].iloc[i] == 'closeLong' and entryLong == 'on':

        entryLong = 'off'
        percent   = ((df['close'].iloc[i]/dataTrade['entryPrice']) * 100) - 100

        if restart:
          profit = (dataTrade['initialBalance'] * percent) / 100
        else:
          profit = (dataTrade['finalBalance'] * percent) / 100

        dataTrade['finalBalance'] += profit
        dataTrade['closePrice']   = df['close'][i]
        dataTrade['dateClose']    = df['date'][i]
        dataTrade['signalC']      = df['LongSignals'][i]

        resume['longProfit'] += profit

        backtestDetail.iloc[-1, backtestDetail.columns.get_loc('finalBalance')] = tradeSigns.truncate(dataTrade['finalBalance'], 2)
        backtestDetail.iloc[-1, backtestDetail.columns.get_loc("closePrice")]   = df['close'][i]
        backtestDetail.iloc[-1, backtestDetail.columns.get_loc("percent")]      = tradeSigns.truncate(percent, 2)
        backtestDetail.iloc[-1, backtestDetail.columns.get_loc("dateClose")]    = df['date'][i]
        backtestDetail.iloc[-1, backtestDetail.columns.get_loc('stopLoss')]     = False
        backtestDetail.iloc[-1, backtestDetail.columns.get_loc('profit')]       = tradeSigns.truncate(profit, 2)

        if (backtestDetail['dateClose'].iloc[-1] - backtestDetail['dateEntry'].iloc[-1]).days == 0:
          backtestDetail.iloc[-1, backtestDetail.columns.get_loc('period')]       = (backtestDetail['dateClose'].iloc[-1] - backtestDetail['dateEntry'].iloc[-1]).seconds/60
        else:
          backtestDetail.iloc[-1, backtestDetail.columns.get_loc('period')]       = (backtestDetail['dateClose'].iloc[-1] - backtestDetail['dateEntry'].iloc[-1]).days
        backtestDetail.iloc[-1, backtestDetail.columns.get_loc('signalClose')]  = df['LongSignals'][i]

        df.loc[i, ('trade')] = 'closeLong'


      #Close long position by stop loss
      elif df['LongSignals'].iloc[i] == 'closeLongSL' and entryLong == 'on':
        
        entryLong = 'off'
        percent   = ((df.loc[i, ('close')]/dataTrade['entryPrice']) * 100) - 100
        if restart:
          profit = (dataTrade['initialBalance'] * percent) / 100
        else:
          profit = (dataTrade['finalBalance'] * percent) / 100

        dataTrade['finalBalance'] += profit
        dataTrade['finalBalance'] += profit
        dataTrade['closePrice']   = df['close'][i]
        dataTrade['dateClose']    = df['date'][i]
        dataTrade['signalC']      = df['LongSignals'][i]

        resume['longCloseBySL'] += 1
        resume['longProfit'] += profit

        backtestDetail.iloc[-1, backtestDetail.columns.get_loc('finalBalance')]  = tradeSigns.truncate(dataTrade['finalBalance'], 2) 
        backtestDetail.iloc[-1, backtestDetail.columns.get_loc('closePrice')]    = df['close'][i]
        backtestDetail.iloc[-1, backtestDetail.columns.get_loc('percent')]       = tradeSigns.truncate(percent, 2)
        backtestDetail.iloc[-1, backtestDetail.columns.get_loc('dateClose')]     = df['date'][i]
        backtestDetail.iloc[-1, backtestDetail.columns.get_loc('stopLoss')]      = True
        backtestDetail.iloc[-1, backtestDetail.columns.get_loc('profit')]        = tradeSigns.truncate(profit, 2)
        backtestDetail.iloc[-1, backtestDetail.columns.get_loc('period')]        = backtestDetail['dateClose'].iloc[-1] - backtestDetail['dateEntry'].iloc[-1]
        backtestDetail.iloc[-1, backtestDetail.columns.get_loc('signalClose')]   = df['LongSignals'][i]
        
        if (backtestDetail['dateClose'].iloc[-1] - backtestDetail['dateEntry'].iloc[-1]).days == 0:
          backtestDetail.iloc[-1, backtestDetail.columns.get_loc('period')]       = (backtestDetail['dateClose'].iloc[-1] - backtestDetail['dateEntry'].iloc[-1]).seconds/60
        else:
          backtestDetail.iloc[-1, backtestDetail.columns.get_loc('period')]       = (backtestDetail['dateClose'].iloc[-1] - backtestDetail['dateEntry'].iloc[-1]).days
        backtestDetail.iloc[-1, backtestDetail.columns.get_loc('signalClose')] = df['LongSignals'][i]

        df.loc[i, ('trade')] = 'closeLongBySL'
        
    return df,resume, backtestDetail, temporalDict



  @staticmethod
  def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper
  
  @staticmethod
  def GetDataFromFile():
    list_of_files = glob.glob('/home/rfeynman/Dropbox/src/BinanceDB/*.csv')
    tmpList = []
    timeFrameList = []
    symbolList = []
    for x in list_of_files:
      tmpString = x[list_of_files[0].find('_')-9:]
      timeFrameList.append(tmpString[tmpString.find('_')+1:tmpString.find('.')])
      symbolList.append(tmpString[tmpString.find('/')+1:tmpString.find('_')])
    #for x in tmpList:
    #  print (x)
    print(timeFrameList)
    print(symbolList)
    df = pd.DataFrame()                                        # this DataFrame var will contain the information of all files found! 


    #for file_name in list_of_files:
    #  print("Reading the file: %s"%file_name)
    #  df = df.append(read_files(file_name), ignore_index=True) # calling the function for each file in the list and append to the general dataframe

    #df = clean_df(df)

def Main():

  ts = tradeSigns()
  #ts.sign("BTCUSDT", "30m")
  #ts.analitic("BTCUSDT", "5m")
  #ts.GetDataFromFile()


if __name__ == '__main__':
  Main()

