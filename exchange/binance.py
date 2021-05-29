#!/usr/bin/python3

import requests 
import json
import decimal
import hmac
import time
import pandas as pd
import hashlib
from decimal import Decimal

import datetime;
from datetime import datetime



#import pytz
#import dateparser
##import datetime

import os.path

from finta import TA


request_delay = 1000

class Binance:


  KLINE_INTERVALS = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']

# init
  def __init__(self, filename = None):

    self.base = 'https://api.binance.com'

    self.endpoints = {
      "klines"       : '/api/v3/klines',
      "exchangeInfo" : '/api/v3/exchangeInfo',
      "averagePrice" : '/api/v3/avgPrice',
      "orderBook"    : '/api/v3/depth',
      "account"      : '/api/v3/account'
    }



  def _get(self, url, params = None, headers = None) -> dict:
    """ Makes a Get Request """
    try: 
      response = requests.get(url, params=params, headers=headers)
      data = json.loads(response.text)
      data['url'] = url
    except Exception as e:
      print("Exception occured when trying to access "+url)
      print(e)
      data = {'code': '-1', 'url':url, 'msg': e}
    return data

  def _post(self, url, params = None, headers = None) -> dict:
    """ Makes a Post Request """
    try: 
      response = requests.post(url, params=params, headers=headers)
      data = json.loads(response.text)
      data['url'] = url
    except Exception as e:
      print("Exception occured when trying to access "+url)
      print(e)
      data = {'code': '-1', 'url':url, 'msg': e}
    return data



  def GetTradingSymbols(self, quoteAssets:list = None):
    ''' Gets All symbols which are tradable (currently) '''
    url = self.base + self.endpoints["exchangeInfo"]
    data = self._get(url)
    if data.__contains__('code'):
      return []

    symbols_list = []
    for pair in data['symbols']:
      if pair['status'] == 'TRADING':
        if quoteAssets != None and pair['quoteAsset'] in quoteAssets:
          symbols_list.append(pair['symbol'])

    return symbols_list

  def GetSymbolDataOfSymbols(self, symbols:list = None):
    ''' Gets All symbols which are tradable (currently) '''
    url = self.base + self.endpoints["exchangeInfo"]
    data = self._get(url)
    if data.__contains__('code'):
      return []

    symbols_list = []

    for pair in data['symbols']:
      if pair['status'] == 'TRADING':
        if symbols != None and pair['symbol'] in symbols:
          symbols_list.append(pair)

    return symbols_list

  def GetSymbolKlinesExtra(self, symbol:str, interval:str, limit:int = 1000, end_time = False):
    # Basicall, we will be calling the GetSymbolKlines as many times as we need 
    # in order to get all the historical data required (based on the limit parameter)
    # and we'll be merging the results into one long dataframe.

    repeat_rounds = 0
    if limit > 1000:
      repeat_rounds = int(limit/1000)
    initial_limit = limit % 1000
    if initial_limit == 0:
      initial_limit = 1000
    # First, we get the last initial_limit candles, starting at end_time and going
    # backwards (or starting in the present moment, if end_time is False)
    df = self.GetSymbolKlines(symbol, interval, limit=initial_limit, end_time=end_time)
    while repeat_rounds > 0:
      # Then, for every other 1000 candles, we get them, but starting at the beginning
      # of the previously received candles.
      df2 = self.GetSymbolKlines(symbol, interval, limit=1000, end_time=df['time'][0])
      df = df2.append(df, ignore_index = True)
      repeat_rounds = repeat_rounds - 1
    
    return df



  def GetSymbolKlines(self, symbol:str, interval:str, limit:int = 1000, end_time = False):
    ''' 
    Gets trading data for one symbol 
    
    Parameters
    --
      symbol str:        The symbol for which to get the trading data

      interval str:      The interval on which to get the trading data
        minutes      '1m' '3m' '5m' '15m' '30m'
        hours        '1h' '2h' '4h' '6h' '8h' '12h'
        days         '1d' '3d'
        weeks        '1w'
        months       '1M;
    '''

    if limit > 1000:
      return self.GetSymbolKlinesExtra(symbol, interval, limit, end_time)
    
    params = '?&symbol='+symbol+'&interval='+interval+'&limit='+str(limit)
    if end_time:
      params = params + '&endTime=' + str(int(end_time))

    url = self.base + self.endpoints['klines'] + params

    # download data
    data = requests.get(url)
    dictionary = json.loads(data.text)

    # put in dataframe and clean-up
    df = pd.DataFrame.from_dict(dictionary)
    df = df.drop(range(6, 12), axis=1)

    # rename columns
    col_names = ['time', 'open', 'high', 'low', 'close', 'volume']
    df.columns = col_names

    # transform values from strings to floats
    for col in col_names:
      df[col] = df[col].astype(float)

    df['date'] = pd.to_datetime(df['time'] * 1000000, infer_datetime_format=True)

    return df


  def GetAvPrice(self, symbol:str):


    url = self.base + self.endpoints['averagePrice']
    params = {
    'symbol': symbol
    }
    return self._get(url, params=params, headers=self.headers)

  def GetPrice(self, symbol:str):


    url = self.base + self.endpoints['price']
    params = {
    'symbol': symbol
    }
    return self._get(url, params=params, headers=self.headers)

  def GetOrderBook(self, symbol:str, limit:int = 100):
    
    params = {
      'symbol': symbol
    }

    if limit != 100:
      params = {
      'symbol': symbol,
      'limit' : limit
      }

    url = self.base + self.endpoints["orderBook"]

    return self._get(url, params=params, headers=self.headers)



  def exportOrderBook(self, symbol:str, limit:int = 100):
    orderbook = self.GetOrderBook(symbol, limit)
    #print(orderbook)
    bids = orderbook['bids']
    asks = orderbook['asks']
    
    price = self.GetPrice(symbol)
    newlist = [[price['price'], 0.0000000]]
    print(newlist)
    df = pd.DataFrame(bids)
    df = df.append(newlist)
    df = df.append(asks)
    df.columns = ['price', 'amount'] 
    df.sort_values(by=['price'], inplace=True)
    #print(df)

    current_time = datetime.datetime.now()
    orderbookfilename = "./download/OrderBook_"+str(current_time.day)+"."+str(current_time.month)+"."+str(current_time.year)+"-"+str(current_time.hour)+"."+str(current_time.minute)+"."+str(current_time.second)+"_"+symbol+".dat"
    df.to_csv(orderbookfilename, sep='\t')


  def exportChart(self, pairlist:list, timeframelist:list, ta:str=False, limit:int=1000):
    
    df = pd.DataFrame()
    
    if ta == True:

      for i in range(0,len(pairlist)):
        print(pairlist[i])

        for e in range(0,len(timeframelist)):
          print(timeframelist[e])

          df = self.GetSymbolKlines(pairlist[i], timeframelist[e], limit)
          df = self.technicalA(df)
          #dataframenName = "./download/DataFrame_"+str(pairlist[i])+"_"+timeframelist[e]+".csv"
          dataframenNameTab = "./download/DataFrame_TAB_"+str(pairlist[i])+"_"+timeframelist[e]+".dat"
          #df.to_csv(dataframenName)
          df.to_csv(dataframenNameTab, sep='\t')

    elif ta == False:
      for i in range(0,len(pairlist)):
        print(pairlist[i])
    
        for e in range(0,len(timeframelist)):
          print(timeframelist[e])
        
          df = self.GetSymbolKlines(pairlist[i], timeframelist[e], limit)
          #dataframenName = "./download/DataFrame_"+str(pairlist[i])+"_"+timeframelist[e]+".csv"
          dataframenNameTab = "./download/DataFrame_"+str(pairlist[i])+"_"+timeframelist[e]+".dat"
          #df.to_csv(dataframenName)
          df.to_csv(dataframenNameTab, sep='\t')




  @staticmethod
  def technicalA(df):


    df['4_ema']  = TA.EMA(df, 4)
    df['9_ema']  = TA.EMA(df, 9)
    df['10_ema'] = TA.EMA(df, 10)
    df['18_ema'] = TA.EMA(df, 18)

    #MACD
    dfMACD= TA.MACD(df)
    dfMACD["HIST"] = dfMACD["MACD"] - dfMACD["SIGNAL"]
    df["MACD"]   = dfMACD["MACD"]
    df["SIGNAL"] = dfMACD["SIGNAL"]
    df["HIST"]   = dfMACD["HIST"]

    #DMI
    dfDMI  = TA.DMI(df)
    df["DI-"] = dfDMI["DI-"]
    df["DI-"] = df["DI-"].fillna(0)

    df["DI+"] = dfDMI["DI+"]
    df["DI+"] = df["DI+"].fillna(0)
    
    
    #ADX
    df["ADX"] = TA.ADX(df)
    df["ADX"] = df["ADX"].fillna(0)

    return df


def Main():

  symbol = 'LINKETH'
  client_id = '43307085'
  exchange = Binance('../credentials.txt')


if __name__ == '__main__':
  Main()
