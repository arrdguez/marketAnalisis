#!/usr/bin/python3


import pandas as pd
from pandas.core.accessor import PandasDelegate

import plotly.graph_objs as go
from plotly.offline import plot

class chart():
  """docstring for chartcreator"""
  def __init__(self):

    pass

  @staticmethod
  def plotData(df, symbol:str, timeframe:str, parameters, TLSR:list):

    color = dict(
      blue   = 'rgba(0, 0, 255, 1)',
      red    = 'rgba(255, 0, 0, 1)',
      green  = 'rgba(0, 128, 0, 1)',
      black  = 'rgba(0, 0, 0, 1)',
      aqua   = 'rgba(0, 255, 255, 1)',
      yellow = 'rgba(255, 255, 0, 1)'
      )


    colordf = pd.DataFrame(columns=['color'])

    ctr = 0

    for i in range(len(TLSR)-1):
      if TLSR[i][1] == '0a':
        colordf.loc[i,'color'] = 'rgba(0,255,108,1)'
      elif TLSR[i][1] == '0b':
        colordf.loc[i,'color'] = 'rgba(0,255,108,1)'
      elif TLSR[i][1] == '0c':
        colordf.loc[i,'color'] = 'Orange'
      elif TLSR[i][1] == '0d':
        colordf.loc[i,'color'] = 'Orange'
      
      elif TLSR[i][1] == '1a':
        colordf.loc[i,'color'] = 'Blue'
      elif TLSR[i][1] == '1b':
        colordf.loc[i,'color'] = 'Blue'
      elif TLSR[i][1] == '1c':
        colordf.loc[i,'color'] = 'Green'
      elif TLSR[i][1] == '1d':
        colordf.loc[i,'color'] = 'Green'
           
      elif TLSR[i][1] == '2a':
        colordf.loc[i,'color'] = 'Orange'
      elif TLSR[i][1] == '2b':
        colordf.loc[i,'color'] = 'rgba(192,32,237,1)'
      elif TLSR[i][1] == '2c':
        colordf.loc[i,'color'] = 'Red'
      elif TLSR[i][1] == '2d':
        colordf.loc[i,'color'] = 'Red'
      
           
      elif TLSR[i][1] == '3a':
        colordf.loc[i,'color'] = 'rgba(192,32,237,1)'
      elif TLSR[i][1] == '3b':
        colordf.loc[i,'color'] = 'rgba(192,32,237,1)'
      elif TLSR[i][1] == '3c':
        colordf.loc[i,'color'] = 'Black'
      elif TLSR[i][1] == '3d':
        colordf.loc[i,'color'] = 'Black'

    colorList = colordf['color'].values.tolist()
    #print(colorList)


    # plot candlestick chart
    candle = go.Candlestick(
      x = df['time'],
      open = df['open'],
      close = df['close'],
      high = df['high'],
      low = df['low'],
      name = "Candlesticks")
    data = [candle]

    for item in parameters:
      if df.__contains__(item['col_name']):
        indicator = go.Scatter(
                x = df['time'],
                y = df[item['col_name']],
             name = item['name'],
             line = dict(color = (color[item['color']])))
        data.append(indicator)

    strategy = go.Scatter(
      x = [item[0] for item in TLSR],
        y = [item[2]  for item in TLSR],
        name = "TLS",
        mode = "markers", 
        marker_symbol="triangle-down",
        marker_color=colorList
        #marker_size = 10
    )
    data.append(strategy)
    # style and display
    # let's customize our layout a little bit:
    plot_title = symbol+"_"+timeframe
    layout = go.Layout(
      title=plot_title,
      xaxis = {
        "title" : symbol+"_"+timeframe,
        "rangeslider" : {"visible": False},
        "type" : "date"
      },
      yaxis = {
        "fixedrange" : False,
      })
      
    fig = go.Figure(data = data, layout = layout)

    plot(fig, filename='../'+plot_title+'.html')