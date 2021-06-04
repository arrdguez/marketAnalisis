#!/usr/bin/python3


import pandas as pd



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

    dfTem['sma'] =  df['close'].rolling(window = length).mean()
    dfTem['highest'] = df["high"].rolling(center=False, window = length).max()
    dfTem['lowest'] = df["low"].rolling(center=False, window = length).min()
    dfTem['aveHL'] = (dfTem['lowest'] + dfTem['highest'])/2
    dfTem['aveHLS'] = (dfTem['aveHL'] + dfTem['sma'])/2
    dfTem['source'] = df['close'] - dfTem['aveHLS']
    dfTem = dfTem.fillna(0)

    yAll = dfTem['source'].values.tolist()
    x = np.array(list(range(0, length))).reshape((-1, 1))

    SMH = []
    for i in range(999,length*2,-1):
      y = np.array(yAll[i-length+1:i+1])

      reg = LinearRegression(fit_intercept = False).fit(x, y)
      SMH.append(reg.predict(x)[-1 ])

    tmp = [0 for _ in range(41)]
    SMH = SMH + tmp
    SMH.reverse()
    dfTem['SMH'] = SMH
    
    if self.setupConfig['export']:
      print("Exporting data ...")
      dfTem.to_csv("./dfTem.csv", sep='\t')
      df.to_csv("./df.csv", sep='\t')

    return SMH

def main():

  #The next code was created to test 
  pass




if __name__ == "__main__":
    main()