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
    if dfSlope['histSlope'][step] > 0 and df['HIST'][step] > 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 1:
      return ['0a', 1]
    elif dfSlope['histSlope'][step] > 0 and df['HIST'][step] > 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 0:
      return ['0b', 2]
    elif dfSlope['histSlope'][step] > 0 and df['HIST'][step] > 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 1:
      return ['0c', 3]
    elif dfSlope['histSlope'][step] > 0 and df['HIST'][step] > 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 0:
      return ['0d', 4]
    elif dfSlope['histSlope'][step] > 0 and df['HIST'][step] < 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 1:
      return ['1a', 5]
    elif dfSlope['histSlope'][step] > 0 and df['HIST'][step] < 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 0:
      return ['1b', 6]
    elif dfSlope['histSlope'][step] > 0 and df['HIST'][step] < 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 1:
      return ['1c', 7]
    elif dfSlope['histSlope'][step] > 0 and df['HIST'][step] < 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 0:
      return ['1d', 8]
    elif dfSlope['histSlope'][step] < 0 and df['HIST'][step] > 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 1:
      return ['2a', 9]
    elif dfSlope['histSlope'][step] < 0 and df['HIST'][step] > 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 0:
      return ['2b', 10]
    elif dfSlope['histSlope'][step] < 0 and df['HIST'][step] > 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 1:
      return ['2c', 11]
    elif dfSlope['histSlope'][step] < 0 and df['HIST'][step] > 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 0:
      return ['2d', 12]
    elif dfSlope['histSlope'][step] < 0 and df['HIST'][step] < 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 1:
      return ['3a', 13]
    elif dfSlope['histSlope'][step] < 0 and df['HIST'][step] < 0 and dfSlope['adxSlope'][step] > 0 and dfSlope['adxStatus'][step] == 0:
      return ['3b', 14]
    elif dfSlope['histSlope'][step] < 0 and df['HIST'][step] < 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 1:
      return ['3c', 15]
    elif dfSlope['histSlope'][step] < 0 and df['HIST'][step] < 0 and dfSlope['adxSlope'][step] < 0 and dfSlope['adxStatus'][step] == 0:
      return ['3d', 16]
    else:
      return '0'

