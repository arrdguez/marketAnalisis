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
  def tlStrategy(df, step:int = 0):
    pass

