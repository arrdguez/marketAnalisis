#!/usr/bin/python3


import pandas as pd
#from aux import Binance
from finta import TA

import numpy as np
from sklearn.linear_model import LinearRegression



class smiHistogram():
  """docstring for smiHistogram"""
  def __init__(self, 
           lengthKC:int = 20, 
             export:bool = False,
             kLinelenght:int = 1000):
    
    self.setupConfig = {
      "lengthKC" : lengthKC,
      'export' : export
    }




  def SMIH(self, df):
    length = self.setupConfig['lengthKC']
    dfTem = pd.DataFrame()
    dfTem['close'] = df['close']
    dfTem['sma'] =  df['close'].rolling(window = length).mean()
    dfTem['highest'] = df["high"].rolling(center=False, window = length).max()
    dfTem['lowest'] = df["low"].rolling(center=False, window = length).min()
    dfTem['aveHL'] = (dfTem['lowest'] + dfTem['highest'])/2
    dfTem['aveHLS'] = (dfTem['aveHL'] + dfTem['sma'])/2
    dfTem['source'] = df['close'] - dfTem['aveHLS']
    dfTem = dfTem.fillna(0)

    yAll = dfTem['source'].values.tolist()
    x = np.array(list(range(1, length+1))).reshape((-1, 1))

    SMH = []
    #print(x)
    #exit()
    for i in range(len(dfTem['close'])-1,length*2,-1):
      y = np.array(yAll[i-length+1:i+1])

      reg = LinearRegression(fit_intercept = True).fit(x, y)
      SMH.append(reg.predict(x)[-1 ])

    tmp = [0 for _ in range(41)]
    SMH = SMH + tmp
    SMH.reverse()
    dfTem['SMH'] = SMH
    #print(dfTem)
    if self.setupConfig['export']:
      print("Exporting data ...")
      dfTem.to_csv("./dfTem.csv", sep='\t')
      df.to_csv("./df.csv", sep='\t')

    return SMH


  def ADX(self, df, printdf:bool = False):
    print("Calculating ADX...")


    period = 14
    adxlen = 14

    df['up'] = df['high'].diff()
    df['down'] = -df['low'].diff()
    df['up'] = df['up'].fillna(0)
    df['down'] = df['down'].fillna(0)

    df['TR'] = TA.TR(df)

    df['truerange'] = TA.SMMA( df, period = 14, column = "TR", adjust = True)
    df['date']= pd.to_datetime(df['date'])

    for i in range(0, len(df['close'])):
      if df.loc[i,"up"] > df.loc[i,"down"] and df.loc[i,"up"] > 0:
        df.loc[i, 'plus'] = df.loc[i, 'up'] # / df.loc[i, 'truerange']
        #df.loc[i, 'plus'] = df.loc[i, 'plus']
      else:
        df.loc[i, 'plus'] = 0

      if df.loc[i,"down"] > df.loc[i,"up"] and df.loc[i,"down"] > 0:
        df.loc[i, 'minus'] = df.loc[i, 'down'] #/ df.loc[i, 'truerange']
        #df.loc[i, 'minus'] = df.loc[i, 'minus']
      else:
        df.loc[i, 'minus'] = 0

    df['plus'] = df['plus'].fillna(0)
    df['minus'] = df['minus'].fillna(0)
    
    df['plus'] = TA.SMMA(df, period=14, column='plus', adjust=True)
    df['minus'] = TA.SMMA(df, period=14, column='minus', adjust=True)
    
    df['plus'] = 100 * df['plus'] / df['truerange']
    df['minus'] = 100 * df['minus'] / df['truerange']

   

    df['sum'] = df['minus'] + df['plus']

    for i in range(0, len(df['sum'])):
      if float(df.loc[i,'sum']) == 0:
        df.loc[i,'tmp'] = abs(df.loc[i,'plus'] - df.loc[i,'minus']) / 1
      else:
        df.loc[i,'tmp'] = abs(df.loc[i,'plus'] - df.loc[i,'minus']) / df.loc[i,'sum'] 

    #print(df['tmp'])
    df['ADX'] =100 * TA.SMMA(df, period=adxlen, column='tmp', adjust=True)
    if printdf:
      df.to_csv("./df.csv", sep='\t')
      print(df['ADX'])
    return(df['ADX'])


def main():

  #The next code was created to test 
  #exchange = Binance()
  #df = exchange.GetSymbolKlines("BTCUSDT", "1h")
  smi = smiHistogram(export = True)
  #smi.SMIH(df)
  smi.ADX(df, printdf = True)
  #print(df)




if __name__ == "__main__":
    main()
