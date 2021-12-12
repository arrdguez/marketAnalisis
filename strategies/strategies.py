import pandas as pd

from finta import TA
from core.SMI import smiHistogram
import math

class Strategies:

  def __init__(self):
    self.SMIH = smiHistogram()

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
      elif df['ADX'][i] >= 23:
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

 
  def SqueezMIndicator(self, df):
    df = self.technicalAnalsis(df)
    dfSlope = self.slopCalculator(df)

    df.loc[0, 'signal'] = '00' 
    df.loc[1, 'signal'] = '00' 
    listResult = ['00', '00']

    for i in range(2, len(df['close'])):

      if dfSlope['histSlope'][i] > 0 and df['SMIH'][i] < 0 and dfSlope['adxSlope'][i] < 0 and dfSlope['adxStatus'][i] == 1:
        df.loc[i, 'signal'] = 'long' #1c
        listResult.append(df.loc[i, 'signal'])
      elif dfSlope['histSlope'][i] > 0 and df['SMIH'][i] < 0 and dfSlope['adxSlope'][i] < 0 and dfSlope['adxStatus'][i] == 0:
        df.loc[i, 'signal'] = 'long' #1d
        listResult.append(df.loc[i, 'signal'])

      elif dfSlope['histSlope'][i] < 0 and df['SMIH'][i] > 0 and dfSlope['adxSlope'][i] < 0 and dfSlope['adxStatus'][i] == 1:
        df.loc[i, 'signal'] = 'short' #2c
        listResult.append(df.loc[i, 'signal'])
      elif dfSlope['histSlope'][i] < 0 and df['SMIH'][i] > 0 and dfSlope['adxSlope'][i] < 0 and dfSlope['adxStatus'][i] == 0:
        df.loc[i, 'signal'] = 'short' #2d
        listResult.append(df.loc[i, 'signal'])

      else:
        df.loc[i, 'signal'] = '00' #else
        listResult.append(df.loc[i, 'signal'])
      

    return df, listResult

  def SslEMA(self, df, emalength:int = 200, smalength:int = 10):

    print('\n\n  **  Evaluating SSL+200EMA strategy  **')

    df = Strategies.SSL(df,emalength = emalength, smalength = smalength)
    print('\n\n  **  The strategy was evaluated  **')
    df['trend'] = ''
    df['signal'] = ''
    #inTheMarket = False
    insideMarketShort = False
    insideMarketLong = False
    longSL = 0.0
    longOpenPrice = 0.0
    shortSL = 0.0
    shortOpenPrice = 0.0

    for i in range(0, len(df['close'])):
      #print(i)

      if df['200_ema'].iloc[i] < df['close'][i]:
        df['trend'].iloc[i] = 'bullish'
      elif df['200_ema'].iloc[i] > df['close'][i]:
        df['trend'].iloc[i] = 'bearish'

      #Taking profit of the long position
      if insideMarketLong and df['sslUp'][i] < df['sslDown'][i] and df['close'][i] > longOpenPrice:
        df['signal'].iloc[i] = 'closeLong'
        insideMarketLong = False
        longOpenPrice = 0.0
        longSL = 0.0

      #Taking profit of the short position
      if insideMarketShort and df['sslUp'][i] > df['sslDown'][i] and df['close'][i] < shortOpenPrice :
        df['signal'].iloc[i] = 'closeShort'
        insideMarketShort = False
        shortOpenPrice = 0.0
        shortSL = 0.0



      if insideMarketLong and df['low'][i] <= longSL:
        df['signal'].iloc[i] = 'closeLongSL'
        insideMarketLong = False
        longOpenPrice = 0.0
        longSL = 0.0

      if insideMarketShort and df['high'][i] >= shortSL:
        df['signal'].iloc[i] = 'closeShortSL'
        insideMarketShort = False
        shortOpenPrice = 0.0
        shortSL = 0.0



      #long entry
      if df['trend'].iloc[i] == 'bullish' and df['sslUp'][i] > df['sslDown'][i] is not insideMarketLong and df['sslUp'][i-1] < df['sslDown'][i-1]:
        df['signal'].iloc[i] = 'long'
        longOpenPrice = df['close'][i]
        insideMarketLong = True
        longSL = df['sslDown'][i]

      #short entry
      elif df['trend'].iloc[i] == 'bearish' and df['sslUp'][i] < df['sslDown'][i] is not insideMarketShort and df['sslUp'][i-1] > df['sslDown'][i-1]:
        df['signal'].iloc[i] = 'short'
        shortOpenPrice = df['close'][i]
        insideMarketShort = True
        shortSL = df['sslDown'][i]


      if df['signal'][i] == '':
        df['signal'].iloc[i] = ' '

    print('  **  The evaluation was finish successfully   **')
    return df


  @staticmethod
  def marginTrade(df, step:int = 0):

    if step >=3:

      if  df['4_ema'][step] > df['9_ema'][step] and  df['9_ema'][step] > df['18_ema'][step]:
        if df['SIGNAL'][step] < df['MACD'][step] and df['open'][step] < df['close'][step]:
          if df['SMIH'][step] > df['SMIH'][step-1] and  df['SMIH'][step-1] > df['SMIH'][step-2]:
          #if df.loc[step:['SMIH']] > dfloc[step:['SMIH']] and  dfloc[step:['SMIH']] > dfloc[step:['SMIH']]:
            return {"signal"   : "BUY"}
          return {"signal"   : "Red candle or the signal is over MACD"}  
        return {"signal"   : "Red candle or the signal is over MACD"}


      elif df['4_ema'][step]< df['9_ema'][step]:
        if df['SIGNAL'][step] > df['MACD'][step]:
          return {"signal"   : "SELL"}
        return {"signal"    : "SELL"}

      else:
        return {"signal"   : "No sell, no buy, just wait!"}

    else:

      if  df['4_ema'][step] > df['9_ema'][step] and  df['9_ema'][step] > df['18_ema'][step]:
        if df['SIGNAL'][step] < df['MACD'][step] and df['open'][step] < df['close'][step]:
          return {"signal"   : "BUY"}
        return {"signal"   : "Red candle or the signal is over MACD"}


      elif df['4_ema'][step]< df['9_ema'][step]:
        if df['SIGNAL'][step] > df['MACD'][step]:
          return {"signal"   : "SELL"}
        return {"signal"    : "SELL"}

      else:
        return {"signal"   : "No sell, no buy, just wait!"}

  @staticmethod
  def tlStrategy(df, dfSlope , step:int = 2):
    if dfSlope['histSlope'][step] > 0 and df['SMIH'][step] > 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 1:
      return [df['time'][step],'0a', '1', df['date'][step]]
    elif dfSlope['histSlope'][step] > 0 and df['SMIH'][step] > 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 0:
      return [df['time'][step],'0b', '2', df['date'][step]]
    elif dfSlope['histSlope'][step] > 0 and df['SMIH'][step] > 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 1:
      return [df['time'][step],'0c', '3', df['date'][step]]
    elif dfSlope['histSlope'][step] > 0 and df['SMIH'][step] > 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 0:
      return [df['time'][step],'0d', '4', df['date'][step]]
    elif dfSlope['histSlope'][step] > 0 and df['SMIH'][step] < 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 1:
      return [df['time'][step],'1a',  '5', df['date'][step]]
    elif dfSlope['histSlope'][step] > 0 and df['SMIH'][step] < 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 0:
      return [df['time'][step],'1b',  '6', df['date'][step]]
    elif dfSlope['histSlope'][step] > 0 and df['SMIH'][step] < 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 1:
      return [df['time'][step],'1c',  '7', df['date'][step]]
    elif dfSlope['histSlope'][step] > 0 and df['SMIH'][step] < 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 0:
      return [df['time'][step],'1d',  '8', df['date'][step]]
    elif dfSlope['histSlope'][step] < 0 and df['SMIH'][step] > 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 1:
      return [df['time'][step],'2a',  '9', df['date'][step]]
    elif dfSlope['histSlope'][step] < 0 and df['SMIH'][step] > 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 0:
      return [df['time'][step],'2b',  '10', df['date'][step]]
    elif dfSlope['histSlope'][step] < 0 and df['SMIH'][step] > 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 1:
      return [df['time'][step],'2c',  '11', df['date'][step]]
    elif dfSlope['histSlope'][step] < 0 and df['SMIH'][step] > 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 0:
      return [df['time'][step],'2d',  '12', df['date'][step]]
    elif dfSlope['histSlope'][step] < 0 and df['SMIH'][step] < 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 1:
      return [df['time'][step],'3a',  '13', df['date'][step]]
    elif dfSlope['histSlope'][step] < 0 and df['SMIH'][step] < 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 0:
      return [df['time'][step],'3b',  '14', df['date'][step]]
    elif dfSlope['histSlope'][step] < 0 and df['SMIH'][step] < 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 1:
      return [df['time'][step],'3c',  '15', df['date'][step]]
    elif dfSlope['histSlope'][step] < 0 and df['SMIH'][step] < 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 0:
      return [df['time'][step],'3d',  '16', df['date'][step]]
    else:

      return '0'

  @staticmethod
  def tlStrategyTWO(df, dfSlope , step:int = 2):
    if dfSlope['histSlope'][step] > 0 and df['SMIH'][step] > 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 1:
      return '0a'
    elif dfSlope['histSlope'][step] > 0 and df['SMIH'][step] > 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 0:
      return '0b'
    elif dfSlope['histSlope'][step] > 0 and df['SMIH'][step] > 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 1:
      return '0c'
    elif dfSlope['histSlope'][step] > 0 and df['SMIH'][step] > 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 0:
      return '0d'
    elif dfSlope['histSlope'][step] > 0 and df['SMIH'][step] < 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 1:
      return '1a'
    elif dfSlope['histSlope'][step] > 0 and df['SMIH'][step] < 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 0:
      return '1b'
    elif dfSlope['histSlope'][step] > 0 and df['SMIH'][step] < 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 1:
      return '1c'
    elif dfSlope['histSlope'][step] > 0 and df['SMIH'][step] < 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 0:
      return '1d'
    elif dfSlope['histSlope'][step] < 0 and df['SMIH'][step] > 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 1:
      return '2a'
    elif dfSlope['histSlope'][step] < 0 and df['SMIH'][step] > 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 0:
      return '2b'
    elif dfSlope['histSlope'][step] < 0 and df['SMIH'][step] > 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 1:
      return '2c'
    elif dfSlope['histSlope'][step] < 0 and df['SMIH'][step] > 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 0:
      return '2d'
    elif dfSlope['histSlope'][step] < 0 and df['SMIH'][step] < 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 1:
      return '3a'
    elif dfSlope['histSlope'][step] < 0 and df['SMIH'][step] < 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 0:
      return '3b'
    elif dfSlope['histSlope'][step] < 0 and df['SMIH'][step] < 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 1:
      return '3c'
    elif dfSlope['histSlope'][step] < 0 and df['SMIH'][step] < 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 0:
      return '3d'
    else:
      #print("histSlope\tSMIH\tadxSlope\tadxStatus")
      #print(str(dfSlope['histSlope'][step])+"\t"+str(df['SMIH'][step])+"\t"+str(dfSlope['adxSlope'][step])+"\t"+str(dfSlope['adxStatus'][step]))
      return 'flat'


  @staticmethod
  def tlStrategyLiveLong(df, dfSlope , step:int = 2):
    if dfSlope['histSlope'][step] > 0 and df['SMIH'][step] > 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 1:
      return '0a'
    elif dfSlope['histSlope'][step] > 0 and df['SMIH'][step] > 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 0:
      return '0b'
    elif dfSlope['histSlope'][step] > 0 and df['SMIH'][step] > 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 1:
      return '0c'
    elif dfSlope['histSlope'][step] > 0 and df['SMIH'][step] > 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 0:
      return '0d'
    elif dfSlope['histSlope'][step] > 0 and df['SMIH'][step] < 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 1:
      return '1a'
    elif dfSlope['histSlope'][step] > 0 and df['SMIH'][step] < 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 0:
      return '1b'
    elif dfSlope['histSlope'][step] > 0 and df['SMIH'][step] < 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 1:
      return '1c'
    elif dfSlope['histSlope'][step] > 0 and df['SMIH'][step] < 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 0:
      return '1d'
    elif dfSlope['histSlope'][step] < 0 and df['SMIH'][step] > 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 1:
      return '2a'
    elif dfSlope['histSlope'][step] < 0 and df['SMIH'][step] > 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 0:
      return '2b'
    elif dfSlope['histSlope'][step] < 0 and df['SMIH'][step] > 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 1:
      return '2c'
    elif dfSlope['histSlope'][step] < 0 and df['SMIH'][step] > 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 0:
      return '2d'
    elif dfSlope['histSlope'][step] < 0 and df['SMIH'][step] < 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 1:
      return '3a'
    elif dfSlope['histSlope'][step] < 0 and df['SMIH'][step] < 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 0:
      return '3b'
    elif dfSlope['histSlope'][step] < 0 and df['SMIH'][step] < 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 1:
      return '3c'
    elif dfSlope['histSlope'][step] < 0 and df['SMIH'][step] < 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 0:
      return '3d'
    else:
      return '0'



  # Util 

  @staticmethod
  def SSL(df, emalength:int = 200, smalength:int = 10):
    print('\n  **  Computing SSL **')
    #print('  **  ', smalength)

    df['200_ema'] = TA.EMA(df, emalength)
    df['smaHigh'] = TA.SMA(df, smalength, column = 'high')
    df['smaLow'] = TA.SMA(df, smalength, column = 'low')

    df['sslDown'] = ''
    df['sslUp'] = ''
    df['Hlv'] = 0 
    for i in range(0, len(df['close'])):
      
      if df['close'].iloc[i] > df['smaHigh'].iloc[i]:
        df['Hlv'].iloc[i] = 1
      elif df['close'].iloc[i] < df['smaLow'].iloc[i]:
        df['Hlv'].iloc[i] = -1
      else:
        df['Hlv'].iloc[i] = df['Hlv'].iloc[i-1] 
      
      if df['Hlv'].iloc[i] < 0:
        df['sslDown'].iloc[i] = df['smaHigh'].iloc[i]
        df['sslUp'].iloc[i] = df['smaLow'].iloc[i]
      else:
        df['sslDown'].iloc[i] = df['smaLow'].iloc[i]
        df['sslUp'].iloc[i] = df['smaHigh'].iloc[i]
    return df


  @staticmethod
  def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper