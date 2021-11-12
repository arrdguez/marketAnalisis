import pandas as pd

from finta import TA
from core.SMI import smiHistogram

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


  def SslEMA(self, df):
    print('  **  Evaluatin SslEMA strategy  **')
    df['200_ema'] = TA.EMA(df, 200)
    


    #SSL

    df['smaHigh'] = TA.SMA(df, 8, column = 'high')
    df['smaLow'] = TA.SMA(df, 8, column = 'low')

    df['sslDown'] = df['close']
    df['sslUp'] = df['close']
    df['trend'] = ''
    df['signal'] = ''
    for i in range(1, len(df['close'])):
      Hlv = df['close'][i]
      if df['close'][i] > df['smaHigh'][i]:
        Hlv /= 1
      elif df['close'][i] < df['smaLow'][i]:
        Hlv /= -1
      else:
        Hlv /= df['close'][i - 1]
      
      if Hlv < 0:
        df['sslDown'][i] = df['smaHigh'][i]
        df['sslUp'][i] = df['smaLow'][i]
      else:
        df['sslDown'][i] = df['smaLow'][i]
        df['sslUp'][i] = df['smaHigh'][i]
  

    for i in range(1, len(df['close'])):
      if df['200_ema'][i] < df['close'][i]:
        df['trend'][i] = 'bullish'
      elif df['200_ema'][i] > df['close'][i]:
        df['trend'][i] = 'bearish'
      if df['trend'][i] == 'bullish' and df['sslUp'][i] > df['sslDown'][i]:
        df['signal'][i] = 'long' 
      elif df['trend'][i] == 'bullish' and df['sslUp'][i] < df['sslDown'][i]:
        df['signal'][i] = 'closeLong' 

      if df['trend'][i] == 'bearish' and df['sslUp'][i] < df['sslDown'][i]:
        df['signal'][i] = 'short' 

      if df['trend'][i] == 'bearish' and df['sslUp'][i] > df['sslDown'][i]:
        df['signal'][i] = 'closeShort' 
      
    for i in range(1, len(df['close'])):

      print(df['trend'][i] +'\t'+df['signal'][i])

    return df
    #plot(sslDown, linewidth=2, color=color.red)
    #plot(sslUp, linewidth=2, color=color.lime)

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
