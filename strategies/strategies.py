import pandas as pd

from finta import TA


class Strategies:

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
      return '0'


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
