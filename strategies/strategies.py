import pandas as pd

from finta import TA


class Strategies:

  @staticmethod
  def marginTrade(df, step:int = 0):

    if step >=3:

      if  df['4_ema'][step] > df['9_ema'][step] and  df['9_ema'][step] > df['18_ema'][step]:
        if df['SIGNAL'][step] < df['MACD'][step] and df['open'][step] < df['close'][step]:
          if df['HIST'][step] > df['HIST'][step-1] and  df['HIST'][step-1] > df['HIST'][step-2]:
          #if df.loc[step:['HIST']] > dfloc[step:['HIST']] and  dfloc[step:['HIST']] > dfloc[step:['HIST']]:
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
    #print(dfSlope)
#    print(dfSlope['histSlope'][step])

    if dfSlope['histSlope'][step] > 0 and df['HIST'][step] > 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 1:
      return '0a'
    elif dfSlope['histSlope'][step] > 0 and df['HIST'][step] > 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 0:
      return '0b'
    elif dfSlope['histSlope'][step] > 0 and df['HIST'][step] > 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 1:
      return '0c'
    elif dfSlope['histSlope'][step] > 0 and df['HIST'][step] > 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 0:
      return '0d'
    elif dfSlope['histSlope'][step] > 0 and df['HIST'][step] < 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 1:
      return '1a'
    elif dfSlope['histSlope'][step] > 0 and df['HIST'][step] < 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 0:
      return '1b'
    elif dfSlope['histSlope'][step] > 0 and df['HIST'][step] < 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 1:
      return '1c'
    elif dfSlope['histSlope'][step] > 0 and df['HIST'][step] < 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 0:
      return '1d'
    elif dfSlope['histSlope'][step] < 0 and df['HIST'][step] > 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 1:
      return '2a'
    elif dfSlope['histSlope'][step] < 0 and df['HIST'][step] > 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 0:
      return '2b'
    elif dfSlope['histSlope'][step] < 0 and df['HIST'][step] > 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 1:
      return '2c'
    elif dfSlope['histSlope'][step] < 0 and df['HIST'][step] > 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 0:
      return '2d'
    elif dfSlope['histSlope'][step] < 0 and df['HIST'][step] < 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 1:
      return '3a'
    elif dfSlope['histSlope'][step] < 0 and df['HIST'][step] < 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 0:
      return '3b'
    elif dfSlope['histSlope'][step] < 0 and df['HIST'][step] < 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 1:
      return '3c'
    elif dfSlope['histSlope'][step] < 0 and df['HIST'][step] < 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 0:
      return '3d'

    
    else:
      return '0'

